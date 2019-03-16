from django.views.generic import ListView, DetailView, TemplateView,\
                            CreateView, UpdateView, DeleteView
from blockuser.models import QuantPolicyOrder
from .models import SanjiaoPolicy
from django.urls import reverse_lazy
from .tasks import run_sanjiao_policy
from django.views.generic.edit import ModelFormMixin
from django.core.urlresolvers import resolve
from django.core.exceptions import ValidationError, ObjectDoesNotExist

ITEMS_PER_PAGE = 5

class addSanjiaoView(CreateView):
    template_name = 'manage/sanjiao/sanjiao_create_form.html'
    model = SanjiaoPolicy
    fields = ['exchange', 'accesskey', 'secretkey', 'symbol', \
              'base_volume', 'start_time', 'end_time', 'symbol1', 'symbol2', 'min_percent']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_name = resolve(self.request.path).url_name
        try:
            quantorder = QuantPolicyOrder.objects.get(user=self.request.user, policy_url_add=url_name)
            context['policy_start_time'] = quantorder.policy_start_time
            context['policy_end_time'] = quantorder.policy_end_time
        except:
            print('no quant order')
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        start_time = form.instance.start_time
        end_time = form.instance.end_time
        url_name = resolve(self.request.path).url_name
        try:
            quantorder = QuantPolicyOrder.objects.get(user=self.request.user, policy_url_add=url_name)
            if quantorder.policy_end_time < end_time:
                raise ValidationError("end time need to be less than %s" %(quantorder.policy_end_time))
            if quantorder.policy_start_time > start_time:
                raise ValidationError("start time need to be more than %s" %(quantorder.policy_start_time))
        except quantorder.DoesNotExist as e:
            print('quantorder does not exist')
        self.object = form.save()
        run_sanjiao_policy.delay(self.object.id)
        return super(ModelFormMixin, self).form_valid(form)

class updateSanjiaoView(UpdateView):
    template_name = 'manage/sanjiao/sanjiao_update_form.html'
    model = SanjiaoPolicy
    queryset = SanjiaoPolicy.objects.all()
    fields = ['exchange', 'accesskey', 'secretkey', 'symbol', \
              'base_volume', 'start_time', 'end_time', 'symbol1', 'symbol2', 'min_percent']

class deleteSanjiaoView(DeleteView):
    template_name = 'manage/sanjiao/sanjiao_delete_form.html'
    model = SanjiaoPolicy
    context_object_name = 'sanjiao_detail'
    success_url = reverse_lazy('manage_getsanjiaolist')

class getSanjiaoDetailView(DetailView):
    queryset = SanjiaoPolicy.objects.all()
    context_object_name = 'sanjiao_detail'
    template_name = 'manage/sanjiao/sanjiao_detail.html'

class getSanjiaoListView(ListView):
    queryset = SanjiaoPolicy.objects.order_by('-update_time')
    template_name = 'manage/sanjiao/sanjiao_list.html'
    context_object_name = 'sanjiao_list'
    paginate_by = ITEMS_PER_PAGE
    
    def get_context_data(self, **kwargs):
        return ListView.get_context_data(self, **kwargs)