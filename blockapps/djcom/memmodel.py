from __future__ import unicode_literals

import copy
import inspect
from itertools import chain
from bisect import bisect
from collections import OrderedDict
from django.core import checks
from django.utils import six
from django.utils.encoding import (force_text, python_2_unicode_compatible,
                                   smart_text, force_str)
from django.utils.datastructures import ImmutableList, OrderedSet
from django.utils.translation import override, string_concat
from django.apps import apps
from django.utils.text import camel_case_to_spaces
from django.db.models.fields import AutoField
from django.utils.functional import cached_property
from django.core.exceptions import FieldDoesNotExist, MultipleObjectsReturned,\
    ObjectDoesNotExist, ValidationError, FieldError
from django.db.models import signals
from django.db.models.fields.reverse_related import ManyToOneRel,\
    ForeignObjectRel
from django.db.models.query_utils import DeferredAttribute, Q
from django.db.models.fields.related import OneToOneField, resolve_relation
from django.db.models.utils import make_model_tuple
from django.db.models.deletion import CASCADE
from django.conf import settings
from django.db.models.manager import ensure_default_manager

PROXY_PARENTS = object()

IMMUTABLE_WARNING = (
    "The return type of '%s' should never be mutated. If you want to manipulate this list "
    "for your own use, make a copy first."
)

DEFAULT_NAMES = ('verbose_name', 'verbose_name_plural', 'db_table', 'ordering',
                 'unique_together', 'permissions', 'get_latest_by',
                 'order_with_respect_to', 'app_label', 'db_tablespace',
                 'abstract', 'managed', 'proxy', 'swappable', 'auto_created',
                 'index_together', 'apps', 'default_permissions',
                 'select_on_save', 'default_related_name',
                 'required_db_features', 'required_db_vendor')

def make_immutable_fields_list(name, data):
    return ImmutableList(data, warning=IMMUTABLE_WARNING % name)

def subclass_exception(name, parents, module, attached_to=None):
    """
    Create exception subclass. Used by ModelBase below.

    If 'attached_to' is supplied, the exception will be created in a way that
    allows it to be pickled, assuming the returned exception class will be added
    as an attribute to the 'attached_to' class.
    """
    class_dict = {'__module__': module}
    return type(name, parents, class_dict)

@python_2_unicode_compatible
class Options(object):
    def __init__(self, meta, app_label=None):
        self._get_fields_cache = {}
        self.proxied_children = []
        self.local_fields = []
        self.local_many_to_many = []
        self.virtual_fields = []
        self.model_name = None
        self.verbose_name = None
        self.verbose_name_plural = None
        self.db_table = ''
        self.ordering = []
        self.select_on_save = False
        self.default_permissions = ('add', 'change', 'delete')
        self.permissions = []
        self.object_name = None
        self.app_label = app_label
        self.get_latest_by = None
        self.required_db_features = []
        self.required_db_vendor = None
        self.meta = meta
        self.pk = None
        self.has_auto_field = False
        self.auto_field = None
        self.abstract = False
        self.managed = True
        self.proxy = False
        # For any class that is a proxy (including automatically created
        # classes for deferred object loading), proxy_for_model tells us
        # which class this model is proxying. Note that proxy_for_model
        # can create a chain of proxy models. For non-proxy models, the
        # variable is always None.
        self.proxy_for_model = None
        # For any non-abstract class, the concrete class is the model
        # in the end of the proxy_for_model chain. In particular, for
        # concrete models, the concrete_model is always the class itself.
        self.concrete_model = None
        self.swappable = None
        self.parents = OrderedDict()
        self.auto_created = False

        # To handle various inheritance situations, we need to track where
        # managers came from (concrete or abstract base classes). `managers`
        # keeps a list of 3-tuples of the form:
        # (creation_counter, instance, abstract(=True))
        self.managers = []

        # List of all lookups defined in ForeignKey 'limit_choices_to' options
        # from *other* models. Needed for some admin checks. Internal use only.
        self.related_fkey_lookups = []

        # A custom app registry to use, if you're making a separate model set.
        self.apps = apps

        self.default_related_name = None

        self.many_to_many = []


    @property
    def label(self):
        return '%s.%s' % (self.app_label, self.object_name)

    @property
    def label_lower(self):
        return '%s.%s' % (self.app_label, self.model_name)

    @property
    def app_config(self):
        # Don't go through get_app_config to avoid triggering imports.
        return self.apps.app_configs.get(self.app_label)

    @property
    def installed(self):
        return self.app_config is not None

    @property
    def abstract_managers(self):
        return [
            (counter, instance.name, instance) for counter, instance, abstract
            in self.managers if abstract
        ]

    @property
    def concrete_managers(self):
        return [
            (counter, instance.name, instance) for counter, instance, abstract
            in self.managers if not abstract
        ]

    def contribute_to_class(self, cls, name):
        from django.db import connection
        from django.db.backends.utils import truncate_name

        cls._meta = self
        self.model = cls
        # First, construct the default values for these options.
        self.object_name = cls.__name__
        self.model_name = self.object_name.lower()
        self.verbose_name = camel_case_to_spaces(self.object_name)

        # Store the original user-defined values for each option,
        # for use when serializing the model definition
        self.original_attrs = {}

        # Next, apply any overridden values from 'class Meta'.
        if self.meta:
            meta_attrs = self.meta.__dict__.copy()
            for name in self.meta.__dict__:
                # Ignore any private attributes that Django doesn't care about.
                # NOTE: We can't modify a dictionary's contents while looping
                # over it, so we loop over the *original* dictionary instead.
                if name.startswith('_'):
                    del meta_attrs[name]
            for attr_name in DEFAULT_NAMES:
                if attr_name in meta_attrs:
                    setattr(self, attr_name, meta_attrs.pop(attr_name))
                    self.original_attrs[attr_name] = getattr(self, attr_name)
                elif hasattr(self.meta, attr_name):
                    setattr(self, attr_name, getattr(self.meta, attr_name))
                    self.original_attrs[attr_name] = getattr(self, attr_name)

            # verbose_name_plural is a special case because it uses a 's'
            # by default.
            if self.verbose_name_plural is None:
                self.verbose_name_plural = string_concat(self.verbose_name, 's')

            # Any leftover attributes must be invalid.
            if meta_attrs != {}:
                raise TypeError("'class Meta' got invalid attribute(s): %s" % ','.join(meta_attrs.keys()))
        else:
            self.verbose_name_plural = string_concat(self.verbose_name, 's')
        del self.meta

        # If the db_table wasn't provided, use the app_label + model_name.
        if not self.db_table:
            self.db_table = "%s_%s" % (self.app_label, self.model_name)
            self.db_table = truncate_name(self.db_table, connection.ops.max_name_length())

    def _prepare(self, model):
        if self.pk is None:
            if self.parents:
                # Promote the first parent link in lieu of adding yet another
                # field.
                field = next(six.itervalues(self.parents))
                # Look for a local field with the same name as the
                # first parent link. If a local field has already been
                # created, use it instead of promoting the parent
                already_created = [fld for fld in self.local_fields if fld.name == field.name]
                if already_created:
                    field = already_created[0]
                field.primary_key = True
                self.setup_pk(field)
            else:
                auto = AutoField(verbose_name='ID', primary_key=True,
                        auto_created=True)
                model.add_to_class('id', auto)

    def add_field(self, field, virtual=False):
        # Insert the given field in the order in which it was created, using
        # the "creation_counter" attribute of the field.
        # Move many-to-many related fields from self.fields into
        # self.many_to_many.
        if virtual:
            self.virtual_fields.append(field)
        elif field.is_relation and field.many_to_many:
            self.local_many_to_many.insert(bisect(self.local_many_to_many, field), field)
        else:
            self.local_fields.insert(bisect(self.local_fields, field), field)
            self.setup_pk(field)

    def setup_pk(self, field):
        if not self.pk and field.primary_key:
            self.pk = field
            field.serialize = False

    def setup_proxy(self, target):
        """
        Does the internal setup so that the current model is a proxy for
        "target".
        """
        self.pk = target._meta.pk
        self.proxy_for_model = target
        self.db_table = target._meta.db_table

    def __repr__(self):
        return '<Options for %s>' % self.object_name

    def __str__(self):
        return "%s.%s" % (smart_text(self.app_label), smart_text(self.model_name))

    def can_migrate(self, connection):
        return False

    @property
    def verbose_name_raw(self):
        """
        There are a few places where the untranslated verbose name is needed
        (so that we get the same value regardless of currently active
        locale).
        """
        with override(None):
            return force_text(self.verbose_name)

    @property
    def swapped(self):
        """
        Has this model been swapped out for another? If so, return the model
        name of the replacement; otherwise, return None.

        For historical reasons, model name lookups using get_model() are
        case insensitive, so we make sure we are case insensitive here.
        """
        return None

    @cached_property
    def fields(self):
        """
        Returns a list of all forward fields on the model and its parents,
        excluding ManyToManyFields.

        Private API intended only to be used by Django itself; get_fields()
        combined with filtering of field properties is the public API for
        obtaining this field list.
        """
        # For legacy reasons, the fields property should only contain forward
        # fields that are not virtual or with a m2m cardinality. Therefore we
        # pass these three filters as filters to the generator.
        # The third lambda is a longwinded way of checking f.related_model - we don't
        # use that property directly because related_model is a cached property,
        # and all the models may not have been loaded yet; we don't want to cache
        # the string reference to the related_model.
        is_not_an_m2m_field = lambda f: not (f.is_relation and f.many_to_many)
        is_not_a_generic_relation = lambda f: not (f.is_relation and f.one_to_many)
        is_not_a_generic_foreign_key = lambda f: not (
            f.is_relation and f.many_to_one and not (hasattr(f.remote_field, 'model') and f.remote_field.model)
        )
        return make_immutable_fields_list(
            "fields",
            (f for f in self._get_fields(reverse=False) if
            is_not_an_m2m_field(f) and is_not_a_generic_relation(f)
            and is_not_a_generic_foreign_key(f))
        )

    @cached_property
    def concrete_fields(self):
        """
        Returns a list of all concrete fields on the model and its parents.

        Private API intended only to be used by Django itself; get_fields()
        combined with filtering of field properties is the public API for
        obtaining this field list.
        """
        return make_immutable_fields_list(
            "concrete_fields", (f for f in self.fields if f.concrete)
        )

    @cached_property
    def local_concrete_fields(self):
        """
        Returns a list of all concrete fields on the model.

        Private API intended only to be used by Django itself; get_fields()
        combined with filtering of field properties is the public API for
        obtaining this field list.
        """
        return make_immutable_fields_list(
            "local_concrete_fields", (f for f in self.local_fields if f.concrete)
        )

    @cached_property
    def fields_map(self):
        res = {}
        fields = self._get_fields(forward=False, include_hidden=True)
        for field in fields:
            res[field.name] = field
            # Due to the way Django's internals work, get_field() should also
            # be able to fetch a field by attname. In the case of a concrete
            # field with relation, includes the *_id name too
            try:
                res[field.attname] = field
            except AttributeError:
                pass
        return res

    def get_field(self, field_name, many_to_many=None):
        """
        Returns a field instance given a field name. The field can be either a
        forward or reverse field, unless many_to_many is specified; if it is,
        only forward fields will be returned.

        The many_to_many argument exists for backwards compatibility reasons;
        it has been deprecated and will be removed in Django 1.10.
        """
        try:
            # Retrieve field instance by name from cached or just-computed
            # field map.
            return self.fields_map[field_name]
        except KeyError:
            raise FieldDoesNotExist('%s has no field named %r' % (self.object_name, field_name))

    def get_base_chain(self, model):
        """
        Return a list of parent classes leading to `model` (ordered from
        closest to most distant ancestor). This has to handle the case where
        `model` is a grandparent or even more distant relation.
        """
        if not self.parents:
            return []
        if model in self.parents:
            return [model]
        for parent in self.parents:
            res = parent._meta.get_base_chain(model)
            if res:
                res.insert(0, parent)
                return res
        return []

    def get_parent_list(self):
        """
        Returns all the ancestors of this model as a list ordered by MRO.
        Useful for determining if something is an ancestor, regardless of lineage.
        """
        result = OrderedSet(self.parents)
        for parent in self.parents:
            for ancestor in parent._meta.get_parent_list():
                result.add(ancestor)
        return list(result)

    def get_ancestor_link(self, ancestor):
        """
        Returns the field on the current model which points to the given
        "ancestor". This is possible an indirect link (a pointer to a parent
        model, which points, eventually, to the ancestor). Used when
        constructing table joins for model inheritance.

        Returns None if the model isn't an ancestor of this one.
        """
        if ancestor in self.parents:
            return self.parents[ancestor]
        for parent in self.parents:
            # Tries to get a link field from the immediate parent
            parent_link = parent._meta.get_ancestor_link(ancestor)
            if parent_link:
                # In case of a proxied model, the first link
                # of the chain to the ancestor is that parent
                # links
                return self.parents[parent] or parent_link

    def _expire_cache(self, forward=True, reverse=True):
        # This method is usually called by apps.cache_clear(), when the
        # registry is finalized, or when a new field is added.
        pass

    def get_fields(self, include_parents=True, include_hidden=False):
        """
        Returns a list of fields associated to the model. By default, includes
        forward and reverse fields, fields derived from inheritance, but not
        hidden fields. The returned fields can be changed using the parameters:

        - include_parents: include fields derived from inheritance
        - include_hidden:  include fields that have a related_name that
                           starts with a "+"
        """
        if include_parents is False:
            include_parents = PROXY_PARENTS
        return self._get_fields(include_parents=include_parents, include_hidden=include_hidden)

    def _get_fields(self, forward=True, reverse=True, include_parents=True, include_hidden=False,
                    seen_models=None):
        """
        Internal helper function to return fields of the model.
        * If forward=True, then fields defined on this model are returned.
        * If reverse=True, then relations pointing to this model are returned.
        * If include_hidden=True, then fields with is_hidden=True are returned.
        * The include_parents argument toggles if fields from parent models
          should be included. It has three values: True, False, and
          PROXY_PARENTS. When set to PROXY_PARENTS, the call will return all
          fields defined for the current model or any of its parents in the
          parent chain to the model's concrete model.
        """
        if include_parents not in (True, False, PROXY_PARENTS):
            raise TypeError("Invalid argument for include_parents: %s" % (include_parents,))
        # This helper function is used to allow recursion in ``get_fields()``
        # implementation and to provide a fast way for Django's internals to
        # access specific subsets of fields.

        # We must keep track of which models we have already seen. Otherwise we
        # could include the same field multiple times from different models.
        topmost_call = False
        if seen_models is None:
            seen_models = set()
            topmost_call = True
        seen_models.add(self.model)

        # Creates a cache key composed of all arguments
        cache_key = (forward, reverse, include_parents, include_hidden, topmost_call)

        try:
            # In order to avoid list manipulation. Always return a shallow copy
            # of the results.
            return self._get_fields_cache[cache_key]
        except KeyError:
            pass

        fields = []
        # Recursively call _get_fields() on each parent, with the same
        # options provided in this call.
        if include_parents is not False:
            for parent in self.parents:
                # In diamond inheritance it is possible that we see the same
                # model from two different routes. In that case, avoid adding
                # fields from the same parent again.
                if parent in seen_models:
                    continue
                if (parent._meta.concrete_model != self.concrete_model and
                        include_parents == PROXY_PARENTS):
                    continue
                for obj in parent._meta._get_fields(
                        forward=forward, reverse=reverse, include_parents=include_parents,
                        include_hidden=include_hidden, seen_models=seen_models):
                    if hasattr(obj, 'parent_link') and obj.parent_link:
                        continue
                    fields.append(obj)

        if forward:
            fields.extend(
                field for field in chain(self.local_fields, self.local_many_to_many)
            )
            # Virtual fields are recopied to each child model, and they get a
            # different model as field.model in each child. Hence we have to
            # add the virtual fields separately from the topmost call. If we
            # did this recursively similar to local_fields, we would get field
            # instances with field.model != self.model.
            if topmost_call:
                fields.extend(
                    f for f in self.virtual_fields
                )

        # In order to avoid list manipulation. Always
        # return a shallow copy of the results
        fields = make_immutable_fields_list("get_fields()", fields)

        # Store result into cache for later access
        self._get_fields_cache[cache_key] = fields
        return fields


class MemModelBase(type):
    """
    Metaclass for all models.
    """
    def __new__(cls, name, bases, attrs):
        super_new = super(MemModelBase, cls).__new__

        # Also ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        parents = [b for b in bases if isinstance(b, MemModelBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        attr_meta = attrs.pop('Meta', None)
        abstract = getattr(attr_meta, 'abstract', False)
        if not attr_meta:
            meta = getattr(new_class, 'Meta', None)
        else:
            meta = attr_meta
        base_meta = getattr(new_class, '_meta', None)

        app_label = None

        # Look for an application configuration to attach the model to.
        app_config = apps.get_containing_app_config(module)

        if getattr(meta, 'app_label', None) is None:
            if app_config is None:
                if not abstract:
                    raise RuntimeError(
                        "Model class %s.%s doesn't declare an explicit "
                        "app_label and isn't in an application in "
                        "INSTALLED_APPS." % (module, name)
                    )

            else:
                app_label = app_config.label

        new_class.add_to_class('_meta', Options(meta, app_label))
        if not abstract:
            new_class.add_to_class(
                'DoesNotExist',
                subclass_exception(
                    str('DoesNotExist'),
                    tuple(
                        x.DoesNotExist for x in parents if hasattr(x, '_meta') and not x._meta.abstract
                    ) or (ObjectDoesNotExist,),
                    module,
                    attached_to=new_class))
            new_class.add_to_class(
                'MultipleObjectsReturned',
                subclass_exception(
                    str('MultipleObjectsReturned'),
                    tuple(
                        x.MultipleObjectsReturned for x in parents if hasattr(x, '_meta') and not x._meta.abstract
                    ) or (MultipleObjectsReturned,),
                    module,
                    attached_to=new_class))
            if base_meta and not base_meta.abstract:
                # Non-abstract child classes inherit some attributes from their
                # non-abstract parent (unless an ABC comes before it in the
                # method resolution order).
                if not hasattr(meta, 'ordering'):
                    new_class._meta.ordering = base_meta.ordering
                if not hasattr(meta, 'get_latest_by'):
                    new_class._meta.get_latest_by = base_meta.get_latest_by

        if getattr(new_class, '_default_manager', None):
            # Multi-table inheritance doesn't inherit default manager from
            # parents.
            new_class._default_manager = None
            new_class._base_manager = None

        # Add all attributes to the class.
        for obj_name, obj in attrs.items():
            new_class.add_to_class(obj_name, obj)

        # All the fields of any type declared on this model
        new_fields = chain(
            new_class._meta.local_fields,
            new_class._meta.local_many_to_many,
            new_class._meta.virtual_fields
        )
        field_names = {f.name for f in new_fields}

        new_class._meta.concrete_model = new_class

        # Collect the parent links for multi-table inheritance.
        parent_links = {}
        for base in reversed([new_class] + parents):
            # Conceptually equivalent to `if base is Model`.
            if not hasattr(base, '_meta'):
                continue
            # Skip concrete parent classes.
            if base != new_class and not base._meta.abstract:
                continue
            # Locate OneToOneField instances.
            for field in base._meta.local_fields:
                if isinstance(field, OneToOneField):
                    related = resolve_relation(new_class, field.remote_field.model)
                    parent_links[make_model_tuple(related)] = field
        # Do the appropriate setup for any model parents.
        for base in parents:
            if not hasattr(base, '_meta'):
                # Things without _meta aren't functional models, so they're
                # uninteresting parents.
                continue

            parent_fields = base._meta.local_fields + base._meta.local_many_to_many
            # Check for clashes between locally declared fields and those
            # on the base classes (we cannot handle shadowed fields at the
            # moment).
            for field in parent_fields:
                if field.name in field_names:
                    raise FieldError(
                        'Local field %r in class %r clashes '
                        'with field of similar name from '
                        'base class %r' % (field.name, name, base.__name__)
                    )
            if not base._meta.abstract:
                # Concrete classes...
                base = base._meta.concrete_model
                base_key = make_model_tuple(base)
                if base_key in parent_links:
                    field = parent_links[base_key]
                #elif not is_proxy:
                else:
                    attr_name = '%s_ptr' % base._meta.model_name
                    field = OneToOneField(
                        base,
                        on_delete=CASCADE,
                        name=attr_name,
                        auto_created=True,
                        parent_link=True,
                    )
                    # Only add the ptr field if it's not already present;
                    # e.g. migrations will already have it specified
                    if not hasattr(new_class, attr_name):
                        new_class.add_to_class(attr_name, field)
                new_class._meta.parents[base] = field
            else:
                base_parents = base._meta.parents.copy()

                # .. and abstract ones.
                for field in parent_fields:
                    new_field = copy.deepcopy(field)
                    new_class.add_to_class(field.name, new_field)
                    # Replace parent links defined on this base by the new
                    # field as it will be appropriately resolved if required.
                    if field.one_to_one:
                        for parent, parent_link in base_parents.items():
                            if field == parent_link:
                                base_parents[parent] = new_field

                # Pass any non-abstract parent classes onto child.
                new_class._meta.parents.update(base_parents)

            # Inherit managers from the abstract base classes.
            new_class.copy_managers(base._meta.abstract_managers)

            # Inherit virtual fields (like GenericForeignKey) from the parent
            # class
            for field in base._meta.virtual_fields:
                if base._meta.abstract and field.name in field_names:
                    raise FieldError(
                        'Local field %r in class %r clashes '
                        'with field of similar name from '
                        'abstract base class %r' % (field.name, name, base.__name__)
                    )
                new_class.add_to_class(field.name, copy.deepcopy(field))

        if abstract:
            # Abstract base models can't be instantiated and don't appear in
            # the list of models for an app. We do the final setup for them a
            # little differently from normal models.
            attr_meta.abstract = False
            new_class.Meta = attr_meta
            return new_class

        new_class._prepare()
        new_class._meta.apps.register_model(new_class._meta.app_label, new_class)
        return new_class

    def copy_managers(cls, base_managers):
        # This is in-place sorting of an Options attribute, but that's fine.
        base_managers.sort()
        for _, mgr_name, manager in base_managers:  # NOQA (redefinition of _)
            val = getattr(cls, mgr_name, None)
            if not val or val is manager:
                new_manager = manager._copy_to_model(cls)
                cls.add_to_class(mgr_name, new_manager)

    def add_to_class(cls, name, value):
        # We should call the contribute_to_class method only if it's bound
        if not inspect.isclass(value) and hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)

    def _prepare(cls):
        """
        Creates some methods once self._meta has been populated.
        """
        opts = cls._meta
        opts._prepare(cls)

        # Give the class a docstring -- its definition.
        if cls.__doc__ is None:
            cls.__doc__ = "%s(%s)" % (cls.__name__, ", ".join(f.name for f in opts.fields))

        get_absolute_url_override = settings.ABSOLUTE_URL_OVERRIDES.get(opts.label_lower)
        if get_absolute_url_override:
            setattr(cls, 'get_absolute_url', get_absolute_url_override)

        ensure_default_manager(cls)
        signals.class_prepared.send(sender=cls)


class ModelState(object):
    """
    A class for storing instance state
    """
    def __init__(self, db=None):
        self.db = db
        # If true, uniqueness validation checks will consider this a new, as-yet-unsaved object.
        # Necessary for correct validation of new instances of objects with explicit (non-auto) PKs.
        # This impacts validation only; it has no effect on the actual save.
        self.adding = True


class MemModel(six.with_metaclass(MemModelBase)):
    _deferred = False

    def __init__(self, *args, **kwargs):
        signals.pre_init.send(sender=self.__class__, args=args, kwargs=kwargs)

        # Set up the storage for instance state
        self._state = ModelState()

        # There is a rather weird disparity here; if kwargs, it's set, then args
        # overrides it. It should be one or the other; don't duplicate the work
        # The reason for the kwargs check is that standard iterator passes in by
        # args, and instantiation for iteration is 33% faster.
        args_len = len(args)
        if args_len > len(self._meta.concrete_fields):
            # Daft, but matches old exception sans the err msg.
            raise IndexError("Number of args exceeds number of fields")

        if not kwargs:
            fields_iter = iter(self._meta.concrete_fields)
            # The ordering of the zip calls matter - zip throws StopIteration
            # when an iter throws it. So if the first iter throws it, the second
            # is *not* consumed. We rely on this, so don't change the order
            # without changing the logic.
            for val, field in zip(args, fields_iter):
                setattr(self, field.attname, val)
        else:
            # Slower, kwargs-ready version.
            fields_iter = iter(self._meta.fields)
            for val, field in zip(args, fields_iter):
                setattr(self, field.attname, val)
                kwargs.pop(field.name, None)
                # Maintain compatibility with existing calls.
                if isinstance(field.remote_field, ManyToOneRel):
                    kwargs.pop(field.attname, None)

        # Now we're left with the unprocessed fields that *must* come from
        # keywords, or default.

        for field in fields_iter:
            is_related_object = False
            # This slightly odd construct is so that we can access any
            # data-descriptor object (DeferredAttribute) without triggering its
            # __get__ method.
            if (field.attname not in kwargs and
                    (isinstance(self.__class__.__dict__.get(field.attname), DeferredAttribute)
                     or field.column is None)):
                # This field will be populated on request.
                continue
            if kwargs:
                if isinstance(field.remote_field, ForeignObjectRel):
                    try:
                        # Assume object instance was passed in.
                        rel_obj = kwargs.pop(field.name)
                        is_related_object = True
                    except KeyError:
                        try:
                            # Object instance wasn't passed in -- must be an ID.
                            val = kwargs.pop(field.attname)
                        except KeyError:
                            val = field.get_default()
                    else:
                        # Object instance was passed in. Special case: You can
                        # pass in "None" for related objects if it's allowed.
                        if rel_obj is None and field.null:
                            val = None
                else:
                    try:
                        val = kwargs.pop(field.attname)
                    except KeyError:
                        # This is done with an exception rather than the
                        # default argument on pop because we don't want
                        # get_default() to be evaluated, and then not used.
                        # Refs #12057.
                        val = field.get_default()
            else:
                val = field.get_default()

            if is_related_object:
                # If we are passed a related instance, set it using the
                # field.name instead of field.attname (e.g. "user" instead of
                # "user_id") so that the object gets properly cached (and type
                # checked) by the RelatedObjectDescriptor.
                setattr(self, field.name, rel_obj)
            else:
                setattr(self, field.attname, val)

        if kwargs:
            for prop in list(kwargs):
                try:
                    if isinstance(getattr(self.__class__, prop), property):
                        setattr(self, prop, kwargs.pop(prop))
                except AttributeError:
                    pass
            if kwargs:
                raise TypeError("'%s' is an invalid keyword argument for this function" % list(kwargs)[0])
        super(MemModel, self).__init__()
        signals.post_init.send(sender=self.__class__, instance=self)

    @classmethod
    def from_db(cls, db, field_names, values):
        if cls._deferred:
            new = cls(**dict(zip(field_names, values)))
        else:
            new = cls(*values)
        new._state.adding = False
        new._state.db = db
        return new

    def __repr__(self):
        try:
            u = six.text_type(self)
        except (UnicodeEncodeError, UnicodeDecodeError):
            u = '[Bad Unicode data]'
        return force_str('<%s: %s>' % (self.__class__.__name__, u))

    def __str__(self):
        if six.PY2 and hasattr(self, '__unicode__'):
            return force_text(self).encode('utf-8')
        return str('%s object' % self.__class__.__name__)

    def __eq__(self, other):
        if not isinstance(other, MemModel):
            return False
        if self._meta.concrete_model != other._meta.concrete_model:
            return False
        my_pk = self._get_pk_val()
        if my_pk is None:
            return self is other
        return my_pk == other._get_pk_val()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        if self._get_pk_val() is None:
            raise TypeError("Model instances without primary key value are unhashable")
        return hash(self._get_pk_val())

    def _get_pk_val(self, meta=None):
        if not meta:
            meta = self._meta
        return getattr(self, meta.pk.attname)

    def _set_pk_val(self, value):
        return setattr(self, self._meta.pk.attname, value)

    pk = property(_get_pk_val, _set_pk_val)

    def serializable_value(self, field_name):
        """
        Returns the value of the field name for this instance. If the field is
        a foreign key, returns the id value, instead of the object. If there's
        no Field object with this name on the model, the model attribute's
        value is returned directly.

        Used to serialize a field's value (in the serializer, or form output,
        for example). Normally, you would just access the attribute directly
        and not use this method.
        """
        try:
            field = self._meta.get_field(field_name)
        except FieldDoesNotExist:
            return getattr(self, field_name)
        return getattr(self, field.attname)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        pass

    def delete(self, using=None, keep_parents=False):
        pass

    delete.alters_data = True
    
    def _get_FIELD_display(self, field):
        value = getattr(self, field.attname)
        return force_text(dict(field.flatchoices).get(value, value), strings_only=True)

    def _get_next_or_previous_by_FIELD(self, field, is_next, **kwargs):
        if not self.pk:
            raise ValueError("get_next/get_previous cannot be used on unsaved objects.")
        op = 'gt' if is_next else 'lt'
        order = '' if is_next else '-'
        param = force_text(getattr(self, field.attname))
        q = Q(**{'%s__%s' % (field.name, op): param})
        q = q | Q(**{field.name: param, 'pk__%s' % op: self.pk})
        qs = self.__class__._default_manager.using(self._state.db).filter(**kwargs).filter(q).order_by(
            '%s%s' % (order, field.name), '%spk' % order
        )
        try:
            return qs[0]
        except IndexError:
            raise self.DoesNotExist("%s matching query does not exist." % self.__class__._meta.object_name)

    def _get_next_or_previous_in_order(self, is_next):
        cachename = "__%s_order_cache" % is_next
        if not hasattr(self, cachename):
            op = 'gt' if is_next else 'lt'
            order = '_order' if is_next else '-_order'
            order_field = self._meta.order_with_respect_to
            filter_args = order_field.get_filter_kwargs_for_object(self)
            obj = self._default_manager.filter(**filter_args).filter(**{
                '_order__%s' % op: self._default_manager.values('_order').filter(**{
                    self._meta.pk.name: self.pk
                })
            }).order_by(order)[:1].get()
            setattr(self, cachename, obj)
        return getattr(self, cachename)

    def clean(self):
        """
        Hook for doing any extra model-wide validation after clean() has been
        called on every field by self.clean_fields. Any ValidationError raised
        by this method will not be associated with a particular field; it will
        have a special-case association with the field defined by NON_FIELD_ERRORS.
        """
        pass

    def full_clean(self, exclude=None):
        """
        Calls clean_fields, clean, and validate_unique, on the model,
        and raises a ``ValidationError`` for any errors that occurred.
        """
        errors = {}
        if exclude is None:
            exclude = []
        else:
            exclude = list(exclude)

        try:
            self.clean_fields(exclude=exclude)
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        # Form.clean() is run even if other validation fails, so do the
        # same with Model.clean() for consistency.
        try:
            self.clean()
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        if errors:
            raise ValidationError(errors)

    def clean_fields(self, exclude=None):
        """
        Cleans all fields and raises a ValidationError containing a dict
        of all validation errors if any occur.
        """
        if exclude is None:
            exclude = []

        errors = {}
        for f in self._meta.fields:
            if f.name in exclude:
                continue
            # Skip validation for empty fields with blank=True. The developer
            # is responsible for making sure they have a valid value.
            raw_value = getattr(self, f.attname)
            if f.blank and raw_value in f.empty_values:
                continue
            try:
                setattr(self, f.attname, f.clean(raw_value, self))
            except ValidationError as e:
                errors[f.name] = e.error_list

        if errors:
            raise ValidationError(errors)

    @classmethod
    def check(cls, **kwargs):
        errors = []
        errors.extend(cls._check_model())
        errors.extend(cls._check_managers(**kwargs))
        errors.extend(cls._check_fields(**kwargs))
        clash_errors = cls._check_id_field() + cls._check_field_name_clashes()
        errors.extend(clash_errors)
        # If there are field name clashes, hide consequent column name
        # clashes.
        if not clash_errors:
            errors.extend(cls._check_column_name_clashes())

        return errors

    @classmethod
    def _check_model(cls):
        errors = []
        if cls._meta.proxy:
            if cls._meta.local_fields or cls._meta.local_many_to_many:
                errors.append(
                    checks.Error(
                        "Proxy model '%s' contains model fields." % cls.__name__,
                        hint=None,
                        obj=None,
                        id='models.E017',
                    )
                )
        return errors

    @classmethod
    def _check_managers(cls, **kwargs):
        """ Perform all manager checks. """

        errors = []
        for __, manager, __ in cls._meta.managers:
            errors.extend(manager.check(**kwargs))
        return errors

    @classmethod
    def _check_fields(cls, **kwargs):
        """ Perform all field checks. """

        errors = []
        for field in cls._meta.local_fields:
            errors.extend(field.check(**kwargs))
        for field in cls._meta.local_many_to_many:
            errors.extend(field.check(from_model=cls, **kwargs))
        return errors

    @classmethod
    def _check_id_field(cls):
        """ Check if `id` field is a primary key. """

        fields = list(f for f in cls._meta.local_fields
            if f.name == 'id' and f != cls._meta.pk)
        # fields is empty or consists of the invalid "id" field
        if fields and not fields[0].primary_key and cls._meta.pk.name == 'id':
            return [
                checks.Error(
                    "'id' can only be used as a field name if the field also "
                    "sets 'primary_key=True'.",
                    hint=None,
                    obj=cls,
                    id='models.E004',
                )
            ]
        else:
            return []

    @classmethod
    def _check_field_name_clashes(cls):
        """ Ref #17673. """

        errors = []
        used_fields = {}  # name or attname -> field

        # Check that multi-inheritance doesn't cause field name shadowing.
        for parent in cls._meta.get_parent_list():
            for f in parent._meta.local_fields:
                clash = used_fields.get(f.name) or used_fields.get(f.attname) or None
                if clash:
                    errors.append(
                        checks.Error(
                            "The field '%s' from parent model "
                            "'%s' clashes with the field '%s' "
                            "from parent model '%s'." % (
                                clash.name, clash.model._meta,
                                f.name, f.model._meta
                            ),
                            hint=None,
                            obj=cls,
                            id='models.E005',
                        )
                    )
                used_fields[f.name] = f
                used_fields[f.attname] = f

        # Check that fields defined in the model don't clash with fields from
        # parents, including auto-generated fields like multi-table inheritance
        # child accessors.
        for parent in cls._meta.get_parent_list():
            for f in parent._meta.get_fields():
                if f not in used_fields:
                    used_fields[f.name] = f

        for f in cls._meta.local_fields:
            clash = used_fields.get(f.name) or used_fields.get(f.attname) or None
            # Note that we may detect clash between user-defined non-unique
            # field "id" and automatically added unique field "id", both
            # defined at the same model. This special case is considered in
            # _check_id_field and here we ignore it.
            id_conflict = (f.name == "id" and
                clash and clash.name == "id" and clash.model == cls)
            if clash and not id_conflict:
                errors.append(
                    checks.Error(
                        "The field '%s' clashes with the field '%s' "
                        "from model '%s'." % (
                            f.name, clash.name, clash.model._meta
                        ),
                        hint=None,
                        obj=f,
                        id='models.E006',
                    )
                )
            used_fields[f.name] = f
            used_fields[f.attname] = f

        return errors

    @classmethod
    def _check_column_name_clashes(cls):
        # Store a list of column names which have already been used by other fields.
        used_column_names = []
        errors = []

        for f in cls._meta.local_fields:
            _, column_name = f.get_attname_column()

            # Ensure the column name is not already in use.
            if column_name and column_name in used_column_names:
                errors.append(
                    checks.Error(
                        "Field '%s' has column name '%s' that is used by "
                        "another field." % (f.name, column_name),
                        hint="Specify a 'db_column' for the field.",
                        obj=cls,
                        id='models.E007'
                    )
                )
            else:
                used_column_names.append(column_name)

        return errors

    @classmethod
    def _check_local_fields(cls, fields, option):
        from django.db import models

        # In order to avoid hitting the relation tree prematurely, we use our
        # own fields_map instead of using get_field()
        forward_fields_map = {
            field.name: field for field in cls._meta._get_fields(reverse=False)
        }

        errors = []
        for field_name in fields:
            try:
                field = forward_fields_map[field_name]
            except KeyError:
                errors.append(
                    checks.Error(
                        "'%s' refers to the non-existent field '%s'." % (
                            option, field_name,
                        ),
                        hint=None,
                        obj=cls,
                        id='models.E012',
                    )
                )
            else:
                if isinstance(field.remote_field, models.ManyToManyRel):
                    errors.append(
                        checks.Error(
                            "'%s' refers to a ManyToManyField '%s', but "
                            "ManyToManyFields are not permitted in '%s'." % (
                                option, field_name, option,
                            ),
                            hint=None,
                            obj=cls,
                            id='models.E013',
                        )
                    )
                elif field not in cls._meta.local_fields:
                    errors.append(
                        checks.Error(
                            ("'%s' refers to field '%s' which is not local "
                             "to model '%s'.") % (
                                option, field_name, cls._meta.object_name,
                            ),
                            hint=("This issue may be caused by multi-table "
                                  "inheritance."),
                            obj=cls,
                            id='models.E016',
                        )
                    )
        return errors
