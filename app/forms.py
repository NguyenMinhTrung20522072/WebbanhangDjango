from django import forms
from .models import ShippingAddress


PAYMENT_CHOICES = (
    ('M', 'Momo'),
    ('P', 'Paypal'),
    ('T', 'Thanh toán khi nhận hàng'),
)
class ShippingAddressForm(forms.ModelForm):
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)
    note = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = ShippingAddress
        fields = ['street_address', 'city', 'state', 'mobile', 'note']