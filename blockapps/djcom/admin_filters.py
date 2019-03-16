from django.contrib.admin.utils import reverse_field_path
from django.contrib.admin.filters import FieldListFilter
from django.utils.encoding import smart_text
from django.db.models import Count

class DistinctChoicesFilter(FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = field_path
        self.lookup_kwarg_isnull = '%s__isnull' % field_path
        self.lookup_val = request.GET.get(self.lookup_kwarg)
        self.lookup_val_isnull = request.GET.get(self.lookup_kwarg_isnull)
        self.empty_value_display = model_admin.get_empty_value_display()
        parent_model, reverse_path = reverse_field_path(model, field_path)
        # Obey parent ModelAdmin queryset when deciding which options to show
        if model == parent_model:
            queryset = model_admin.get_queryset(request)
        else:
            queryset = parent_model._default_manager.all()
        self.lookup_choices = queryset.values(field.name).annotate(the_count=Count(field.name)).order_by(field.name)
        super(DistinctChoicesFilter, self).__init__(
            field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg_isnull]

    def choices(self, cl):
        yield {
            'selected': (self.lookup_val is None
                and self.lookup_val_isnull is None),
            'query_string': cl.get_query_string({},
                [self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('All'),
        }
        include_none = False
        for item in self.lookup_choices:
            val = item[self.field.name]
            count = item['the_count']
            if val is None:
                include_none = True
                continue
            val = smart_text(val)
            name = self._getChoiceName(val)
            if name is None: name = val
            yield {
                'selected': self.lookup_val == val,
                'query_string': cl.get_query_string({
                    self.lookup_kwarg: val,
                }, [self.lookup_kwarg_isnull]),
                'display': '%s (%s)' % (name, count),
            }
        if include_none:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': cl.get_query_string({
                    self.lookup_kwarg_isnull: 'True',
                }, [self.lookup_kwarg]),
                'display': self.empty_value_display,
            }

    def _getChoiceName(self, val):
        for lookup, title in self.field.flatchoices:
            if lookup is None: continue
            if str(lookup) == val:
                return title
        else:
            return None
