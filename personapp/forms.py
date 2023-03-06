from django.forms import ModelForm, ValidationError
from django import forms
from .models import Person

class PersonForm(ModelForm):

  class Meta:
    model = Person
    fields = ('firstname', 'lastname', 'email', 'phone', 'bio')

    widgets = {
      'firstname':forms.TextInput(attrs={'class':'form-control'}),
      'lastname':forms.TextInput(attrs={'class':'form-control'}),
      'email':forms.TextInput(attrs={'class':'form-control'}),
      'phone':forms.TextInput(attrs={'class':'form-control'}),
      'bio':forms.Textarea(attrs={'class':'form-control'}),
    }

  
  def clean_firstname(self):
    firstname = self.cleaned_data['firstname']
    if len(str(firstname))<4:
      raise ValidationError('Firstname must be more than or equal to 4 characters')
    
    return firstname
  
  def clean_lastname(self):
    lastname = self.cleaned_data['lastname']
    if len(str(lastname))<4:
      raise ValidationError('Lastname must be more than or equal to 4 characters')
    
    return lastname
  
  
  
  
  
  