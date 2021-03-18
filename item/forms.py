from django import forms
from .models import OrderInfo

class CheckoutForm(forms.ModelForm):
    Email = forms.EmailField(required=False)

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Email'].disabled = True
    class Meta:
        model = OrderInfo
        fields = ['Email' ,'name' ,'address', 'phonenumber']
    