from django import forms
from products.models import Payment
from django.utils.translation import gettext_lazy as _


c={'s':'stripe','p':'paypal'}
class Checkoutform(forms.ModelForm):
    #PaymentMethod=forms.ChoiceField(widget=forms.RadioSelect,choices=c)
    def __init__(self, *args, **kwargs):
        super(Checkoutform, self).__init__(*args, **kwargs)

        # change a widget attribute:
        #self.fields['shipment_phone'].widget.attrs["size"] = 5
        self.fields['shipment_phone'].widget.attrs["class"] = 'form-control'
        self.fields['security_code'].widget.attrs["class"] = 'form-control'
        self.fields['shipment_address'].widget.attrs["class"] = 'form-control'
        self.fields['card_number'].widget.attrs["class"] = 'form-control'
        self.fields['expire'].widget.attrs["class"] = 'form-control'
        
        

    class Meta:
        model=Payment
        fields=['shipment_address','shipment_phone','card_number','expire','security_code']
        #exclude=['PaymentMethod']
        #labels = {'shipment_address': _('Writer'),}
        #help_texts = {'shipment_phone': _('Some useful help text.'),}
        #widget = {'shipment_phone':forms.TextInput(attrs={'cols': 200, 'rows': 200}),}
        