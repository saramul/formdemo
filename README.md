# formdemo with django
## contents
### models
```
from django.db import models

# Create your models here.
class Contact(models.Model):
  firstname = models.CharField(max_length=20)
  lastname = models.CharField(max_length=20)
  company = models.CharField(max_length=20)
  mobile = models.CharField(max_length=10)

  def __str__(self):
    return self.firstname
```
### forms
```
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
  
```
### views
```
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contact
from django.contrib import messages

# Create your views here.
def contacts(request):
  contacts = Contact.objects.all()
  context = {
    'title': 'Show My Contacts',
    'contacts': contacts
  }
  return render(request, 'contact/show_all.html', context)

def new_contact(request): 
  
  if request.method == 'POST':
    form = ContactForm(request.POST)
    if form.is_valid():
      firstname = form.cleaned_data['firstname']
      lastname = form.cleaned_data['lastname']
      company = form.cleaned_data['company']
      mobile = form.cleaned_data['mobile']

      contact = Contact(firstname=firstname, lastname=lastname, company=company, mobile=mobile)
      contact.save()
      
      messages.success(request, 'Add New Contact Successfull.')
      return redirect(to='contactapp:show_all')
    
    else:
      pass

  else:
    form = ContactForm(None)
    

  return render(request, 'contact/new_contact.html', {'title':'New Contact', 'form':form})

def update_contact(request, id):
  contact = Contact.objects.get(pk=id)
  if request.method == 'POST':
    form = ContactForm(request.POST)
    if form.is_valid():
      contact.firstname = form.cleaned_data['firstname']
      contact.lastname = form.cleaned_data['lastname']
      contact.company = form.cleaned_data['company']
      contact.mobile = form.cleaned_data['mobile']

      contact.save()
      
      messages.success(request, 'Update Contact Successfully!')
      return redirect(to='contactapp:show_all')

  else:
    form = ContactForm(initial=
            {
              'firstname':contact.firstname,
              'lastname':contact.lastname,
              'company':contact.company,
              'mobile':contact.mobile,
              
            })

  context = {
    'title':'Update Contact',
    'form': form,
    
  }

  return render(request, 'contact/update_contact.html', context)

def delete_contact(request, id):
  contact = Contact.objects.get(pk=id)
  contact.delete()

  messages.success(request, 'Delete contact Successfully!')

  return redirect(to='contactapp:show_all')
  ```
  ###urls
  ```
  from django.urls import path
from . import views

app_name = 'contactapp'
urlpatterns = [
    path('show_all/', views.contacts, name='show_all'),
    path('new_contact/', views.new_contact, name='new_contact'),
    path('<int:id>/update_contact/', views.update_contact, name='update_contact'),
    path('<int:id>/delete_contact/', views.delete_contact, name='delete_contact'),
]
  ```
