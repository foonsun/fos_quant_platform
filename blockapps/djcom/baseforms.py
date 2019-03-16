from django import forms

class BaseForm(forms.Form):
    def __init__(self, data, *args, **kwargs):
        if not data:
            data = None
        super(BaseForm, self).__init__(data, *args, **kwargs)
