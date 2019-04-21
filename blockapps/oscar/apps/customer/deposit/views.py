from django.views import generic
from oscar.core.loading import get_class, get_model
from oscar_accounts.checkout import gateway
from django.conf import settings

AbstractDepositRecords = get_model('customer', 'AbstractDepositRecords')

PageTitleMixin = get_class('customer.mixins', 'PageTitleMixin')

class AccountDepositView(generic.TemplateView):
    template_name = 'customer/deposit/deposit.html'
    
    def get_context_data(self, **kwargs):
        context = super(AccountDepositView, self).get_context_data(**kwargs)
        context['source'] = 'EOS'
        context['address'] = settings.EOS_WALLET_ADDRESS
        useraccount = gateway.user_accounts(self.request.user)[0]
        context['tag'] = useraccount.code
        return context

class AccountDepositListView(PageTitleMixin, generic.ListView):
    context_object_name = active_tab = "deposit_lists"
    template_name = 'customer/deposit/deposit_list.html'
    page_title = _('充值记录')

    def get_queryset(self):
        useraccount = gateway.user_accounts(self.request.user)[0]
        return AbstractDepositRecords.objects.filter(memo=useraccount.code)