from django.views.generic import ListView, DetailView, TemplateView,\
                            CreateView, UpdateView, DeleteView
from blockuser.models import QuantPolicy, QuantPolicyOrder
from django.urls import reverse_lazy
from django.views.generic.edit import ModelFormMixin
from django.core.urlresolvers import resolve
from django.core.exceptions import ValidationError

ITEMS_PER_PAGE = 5

class getQuantListView(ListView):
    queryset = QuantPolicy.objects.order_by('-update_time')
    context_object_name = 'quant_policy_list'
    template_name = 'product/quant_policy_list.html'
    paginate_by = ITEMS_PER_PAGE
    
class getQuantDetailView(DetailView):
    queryset = QuantPolicy.objects.all()
    context_object_name = 'quant_policy_detail'
    template_name = 'product/quant_policy_detail.html'

class manageIndexView(TemplateView):
    template_name = 'manage/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(manageIndexView, self).get_context_data(**kwargs)
        context['quantpolicyorder'] = QuantPolicyOrder.objects.filter(user=self.request.user)
        return context