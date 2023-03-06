from django import forms
from django.core.validators import RegexValidator

def start_with_cap_letter(value):
  if str(value[0]).islower():
    raise forms.ValidationError('The text should startwith Capital Letter.')
  

class ContactForm(forms.Form):
  firstname = forms.CharField(label='Firstname', min_length=4, max_length=20,  widget=forms.TextInput(attrs={'class':'form-control'}), validators=[start_with_cap_letter,])
  lastname = forms.CharField(label='Lastname', min_length=4, max_length=20,  widget=forms.TextInput(attrs={'class':'form-control'}), validators=[start_with_cap_letter])
  company = forms.CharField(label='Company',  widget=forms.TextInput(attrs={'class':'form-control'}), validators=[start_with_cap_letter])
  mobile = forms.CharField(label='Mobile Phone', max_length=12, widget=forms.TextInput(attrs={'class':'form-control'}), 
                           validators=[RegexValidator('[0]\d[-]\d{4}[-]\d{4}',message='enter mobile number format 0x-xxxx-xxxx')])
  
