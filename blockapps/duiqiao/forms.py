from django import forms
from django.forms import ModelForm

'''
class DuiqiaoForm(ModelForm):
    class Meta:
        model = DuiQiaoPolicy
        fields = ['exchange', 'accesskey', 'secretkey', 'symbol', 'max_buy_price',\
                   'min_sell_price', 'percent_balance', 'start_time', 'end_time']
    def __init__(self, *args, **kwargs):
        self.user = self.request.user
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance
'''     