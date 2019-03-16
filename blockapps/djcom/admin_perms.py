from __future__ import unicode_literals

from collections import OrderedDict

from django.contrib import admin
from django.contrib.admin.options import TO_FIELD_VAR
from django.contrib.admin.templatetags.admin_modify import \
    submit_row as original_submit_row
from django.contrib.admin.templatetags.admin_modify import register
from django.contrib.admin.utils import flatten, unquote
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth import get_permission_codename
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _

#from .utils import get_model_name

import django
from django.contrib.auth.management import _get_all_permissions

from django.db import models

class DjangoVersion(object):
    DJANGO_18, DJANGO_19, DJANGO_110, DJANGO_111 = range(0, 4)

def django_version():
    if django.get_version().startswith('1.8'):
        return DjangoVersion.DJANGO_18
    elif django.get_version().startswith('1.9'):
        return DjangoVersion.DJANGO_19
    elif django.get_version().startswith('1.10'):
        return DjangoVersion.DJANGO_110
    elif django.get_version().startswith('1.11'):
        return DjangoVersion.DJANGO_111

def get_model_name(model):
    if django_version() == DjangoVersion.DJANGO_18:
        return '%s.%s' % (model._meta.app_label, model._meta.object_name)

    return model._meta.label

def get_all_permissions(opts, ctype=None):
    if django_version() < DjangoVersion.DJANGO_110:
        return _get_all_permissions(opts, ctype)

    return _get_all_permissions(opts)

class PermissionsMixin(models.Model):
    """
        Mixin adds view permission to model.
    """
    class Meta:
        abstract=True
        default_permissions = ('add', 'change', 'delete', 'view')

@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    """submit buttons context change"""
    ctx = original_submit_row(context)
    ctx.update({
        'show_save_as_new': context.get(
            'show_save_as_new', ctx['show_save_as_new']),
        'show_save_and_add_another': context.get(
            'show_save_and_add_another', ctx['show_save_and_add_another']),
        'show_save_and_continue': context.get(
            'show_save_and_continue', ctx['show_save_and_continue']),
        'show_save': context.get(
            'show_save', ctx['show_save']),
    })
    return ctx


class PermChangeList(ChangeList):
    def __init__(self, *args, **kwargs):
        super(PermChangeList, self).__init__(*args, **kwargs)
        # TODO: Exam if is None
        self.request = args[0]

        # If user has only view permission change the title of the changelist
        # view
        if self.model_admin.has_view_permission(self.request) and \
                not self.model_admin._has_change_only_permission(self.request):
            if self.is_popup:
                title = _('Select %s')
            else:
                title = _('Select %s to view')
            self.title = title % force_text(self.opts.verbose_name)


class PermBaseModelAdmin(admin.options.BaseModelAdmin):
    def _has_change_only_permission(self, request, obj=None):
        return super(PermBaseModelAdmin,
                     self).has_change_permission(request, obj)

    def get_model_perms(self, request):
        """
        Returns a dict of all perms for this model. This dict has the keys
        ``add``, ``change``, ``delete`` and ``view`` mapping to the True/False
        for each of those actions.
        """
        return {
            'add': self.has_add_permission(request),
            'change': self.has_change_permission(request),
            'delete': self.has_delete_permission(request),
            'view': self.has_view_permission(request)
        }

    def has_view_permission(self, request, obj=None):
        """
        Returns True if the given request has permission to view an object.
        Can be overridden by the user in subclasses.
        """
        opts = self.opts
        codename = get_permission_codename('view', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def has_change_permission(self, request, obj=None):
        """
        Override this method in order to return True whenever a user has view
        permission and avoid re-implementing the change_view and
        changelist_view views. Also, added an extra argument to determine
        whenever this function will return the original response
        """
        change_permission = super(PermBaseModelAdmin,
                                  self).has_change_permission(request, obj)
        if change_permission or self.has_view_permission(request, obj):
            return True
        else:
            return change_permission

    def get_excluded_fields(self):
        """
        Check if we have no excluded fields defined as we never want to
        show those (to any user)
        """
        if self.exclude is None:
            exclude = []
        else:
            exclude = list(self.exclude)

        # logic taken from: django.contrib.admin.options.ModelAdmin#get_form
        if self.exclude is None and hasattr(
                self.form, '_meta') and self.form._meta.exclude:
            # Take the custom ModelForm's Meta.exclude into account only
            # if the ModelAdmin doesn't define its own.
            exclude.extend(self.form._meta.exclude)

        return exclude

    def get_fields(self, request, obj=None):
        """
        If the user has only the view permission return these readonly fields
        which are in fields attr
        """
        if ((self.has_view_permission(request, obj) and (
            obj and not self._has_change_only_permission(request, obj))) or (
                obj is None and not self.has_add_permission(request))):
            fields = super(
                PermBaseModelAdmin,
                self).get_fields(request, obj)
            excluded_fields = self.get_excluded_fields()
            readonly_fields = self.get_readonly_fields(request, obj)
            new_fields = [i for i in flatten(fields) if
                          i in readonly_fields and
                          i not in excluded_fields]

            return new_fields
        else:
            return super(PermBaseModelAdmin, self).get_fields(
                request, obj)

    def get_readonly_fields(self, request, obj=None):
        """
        Return all fields as readonly for the view permission
        """
        # get read_only fields specified on the admin class is available
        # (needed for @property fields)
        readonly_fields = super(PermBaseModelAdmin,
                                self).get_readonly_fields(request, obj)

        if ((self.has_view_permission(request, obj) and (
            obj and not self._has_change_only_permission(request, obj))) or (
                obj is None and not self.has_add_permission(request))):
            readonly_fields = (
                list(readonly_fields) +
                [field.name for field in self.opts.fields
                 if field.editable] +
                [field.name for field in self.opts.many_to_many
                 if field.editable]
            )

            # Try to remove id if user has not specified fields and
            # readonly fields
            try:
                readonly_fields.remove('id')
            except ValueError:
                pass

            if self.fields:
                # Set as readonly fields the specified fields
                readonly_fields = flatten(self.fields)

            # Remove from the readonly_fields list the excluded fields
            # specified on the form or the modeladmin
            excluded_fields = self.get_excluded_fields()
            if excluded_fields:
                readonly_fields = [
                    f for f in readonly_fields if f not in excluded_fields
                ]

        return tuple(readonly_fields)

    def get_actions(self, request):
        """
        Override this funciton to remove the actions from the changelist view
        """
        actions = super(PermBaseModelAdmin, self).get_actions(
            request)

        if self.has_view_permission(request) and \
                not self._has_change_only_permission(request):
            # If the user doesn't have delete permission return an empty
            # OrderDict otherwise return only the default admin_site actions
            if not self.has_delete_permission(request):
                return OrderedDict()
            else:
                return OrderedDict(
                    (name, (func, name, desc))
                    for func, name, desc in actions.values()
                    if name in dict(self.admin_site.actions).keys()
                )

        return actions


class PermInlineModelAdmin(PermBaseModelAdmin,
                                          admin.options.InlineModelAdmin):
    def get_queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        if self.has_view_permission(request) and \
                not self._has_change_only_permission(request):
            return super(PermInlineModelAdmin, self)\
                .get_queryset(request)
        else:
            # TODO: Somehow super executes admin.options.InlineModelAdmin
            # get_queryset and PermBaseModelAdmin which is
            # convinient
            return super(PermInlineModelAdmin, self)\
                .get_queryset(request)


class PermModelAdmin(PermBaseModelAdmin,
                                    admin.ModelAdmin):
    def get_changelist(self, request, **kwargs):
        """
        Returns the ChangeList class for use on the changelist page.
        """
        return PermChangeList

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        for inline_class in self.inlines:
            new_class = type(
                str('DynamicAdminViewPermissionInlineModelAdmin'),
                (inline_class, PermInlineModelAdmin),
                dict(inline_class.__dict__))

            inline = new_class(self.model, self.admin_site)
            if request:
                if not (inline.has_view_permission(request, obj) or
                        inline.has_add_permission(request) or
                        inline._has_change_only_permission(request, obj) or
                        inline.has_delete_permission(request, obj)):
                    continue
                if inline.has_view_permission(request, obj) and \
                        not inline._has_change_only_permission(request, obj):
                    inline.can_delete = False
                if not inline.has_add_permission(request):
                    inline.max_num = 0
            inline_instances.append(inline)

        return inline_instances

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Override this function to hide the sumbit row from the user who has
        view only permission
        """
        to_field = request.POST.get(
            TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR)
        )
        model = self.model
        opts = model._meta

        # TODO: Overriding the change_view costs 1 query more (one from us
        # and another from the super)
        obj = self.get_object(request, unquote(object_id), to_field)

        if self.has_view_permission(request, obj) and \
                not self._has_change_only_permission(request, obj):
            extra_context = extra_context or {}
            extra_context['title'] = _('View %s') % force_text(
                opts.verbose_name)

            extra_context['show_save'] = False
            extra_context['show_save_and_continue'] = False
            extra_context['show_save_and_add_another'] = False
            extra_context['show_save_as_new'] = False

            inlines = self.get_inline_instances(request, obj)
            for inline in inlines:
                if (inline._has_change_only_permission(request, obj) or
                        inline.has_add_permission(request)):
                    extra_context['show_save'] = True
                    extra_context['show_save_and_continue'] = True
                    break

        return super(PermModelAdmin, self).change_view(
            request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        resp = super(PermModelAdmin, self).changelist_view(
            request, extra_context)
        if self.has_view_permission(request) and \
                not self._has_change_only_permission(request):
            if hasattr(resp, 'context_data'):
                # 'HttpResponseRedirect' object has no attribute 'context_data'
                # when execute action and redirect back to change list.
                resp.context_data['cl'].formset = None

        return resp
