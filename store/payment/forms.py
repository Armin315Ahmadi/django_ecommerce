from django import forms
from.models import ShippingAddress
class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Full_name'}),required=True)
    shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'email address'}),required=True)
    shipping_address1 = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'address1'}),required=True)
    shipping_address2 = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'address2'}),required=False)
    shipping_city = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'city'}),required=True)
    shipping_state = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'state'}),required=False)
    shipping_zipcode = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'zipcode'}),required=False)
    shipping_country = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'country'}),required=True)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name','shipping_email','shipping_address1'
                    ,'shipping_address2','shipping_city',
                  'shipping_state','shipping_zipcode','shipping_country']
        exclude = ['user',]
