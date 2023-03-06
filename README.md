# formdemo with django
## python code
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
  ### urls
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
## templates
### show_all
```
{% extends 'layout.html' %}

{% block title %}
  {{title}}
{% endblock %}

{% block content %}
  <div class="container mt-4">
    <h3>{{title}}</h3>
    <hr>
    <div class="row">
      <div class="col-12">
        <a href="{% url 'contactapp:new_contact' %}" class="btn btn-outline-success float-end"><i class="bi bi-person-add"></i> Add New Contact</a>
      </div>
    </div>
    <div class="table-responsive mt-4">
      <div class="card">
        <div class="card-header bg-success text-center text-light">
          <h4>{{title}}</h4>
        </div>
        <div class="card-body">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>#</th>
                <th>Firstname</th>
                <th>Lastname</th>
                <th>Company</th>
                <th>Mobile Phone</th>
                <th>Action</th>
              </tr>
            </thead>
            {% for contact in contacts %}
              <tr>
                <td>{{forloop.counter}}</td>
                <td>{{contact.firstname}}</td>
                <td>{{contact.lastname}}</td>
                <td>{{contact.company}}</td>
                <td>{{contact.mobile}}</td>
                <td>
                  <a href="{% url 'contactapp:update_contact' id=contact.id %}" class="btn btn-outline-success btn-sm"><i class="bi bi-person-check"></i></a>
                  <a onclick="return confirm('Are you sure to delete this contact?')" href="{% url 'contactapp:delete_contact' id=contact.id %}" class="btn btn-outline-danger btn-sm"><i class="bi bi-person-x"></i></a>
                </td>
              </tr>
            {% endfor %}
            
          </table>
        </div>
      </div>
    </div>
  </div>
{% endblock %}
```
### new_contact
```
{% extends 'layout.html' %}

{% block title %}
  {{title}}
{% endblock %}

{% block content %}
  <div class="container mt-4">
    <h3>{{title}}</h3>
    <hr>
    
    <div class="card mt-3 mb-4">
      <div class="card-header bg-success text-center text-light">
        <h4>{{title}}</h4>
      </div>
      <div class="card-body">
        <form method="post" novalidate>
          {% csrf_token %}

          <div class="mb-3">
            <label class="form-label">{{form.firstname.label}}</label>
            {% if form.errors %}
            {{form.firstname}}
            <div class="text-danger">
              {% for error in form.firstname.errors %}
                <span>{{error}}</span>
              {% endfor %}
            </div>
            
            {% else %}
            {{form.firstname}}
            {% endif %}
            
            
          </div>
          <div class="mb-3">
            <label class="form-label">{{form.lastname.label}}</label>
            {{form.lastname}}
            <div class="text-danger">
              {% for error in form.lastname.errors %}
                  <span>{{error}}</span>
              {% endfor %}
              
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">{{form.company.label}}</label>
            {{form.company}}
            <div class="text-danger">
              {% for error in form.company.errors %}
                  <span>{{error}}</span>
              {% endfor %}
              
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">{{form.mobile.label}}</label>
            {{form.mobile}}
            <div class="text-danger">
              {% for error in form.mobile.errors %}
                  <span>{{error}}</span>
              {% endfor %}
              
            </div>
          </div>
          <div class="mb-3 text-center mt-5">
            <button type="submit" class="btn btn-outline-success"><i class="bi bi-person-add"></i> New Contact</button>
          </div>
        </form>
      </div>
    </div>
    
  </div>
{% endblock %}

```
### update_contact
```
{% extends 'layout.html' %}

{% block title %}
  {{title}}
{% endblock %}

{% block content %}
  <div class="container mt-4">
    <h3>{{title}}</h3>
    <hr>
    
    <div class="card mt-3 mb-4">
      <div class="card-header bg-success text-center text-light">
        <h4>{{title}}</h4>
      </div>
      <div class="card-body">
        <form method="post" novalidate>
          {% csrf_token %}

          <div class="mb-3">
            <label class="form-label">{{form.firstname.label_tag}}</label>
            {% if form.errors %}
            {{form.firstname}}
            <div class="text-danger">
              {% for error in form.firstname.errors %}
                <span>{{error}}</span>
              {% endfor %}
            </div>
            
            {% else %}
            {{form.firstname}}
            {% endif %}
            
            
          </div>
          <div class="mb-3">
            <label class="form-label">{{form.lastname.label_tag}}</label>
            {{form.lastname}}
            <div class="text-danger">
              {% for error in form.lastname.errors %}
                  <span>{{error}}</span>
              {% endfor %}
              
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">{{form.company.label_tag}}</label>
            {{form.company}}
            <div class="text-danger">
              {% for error in form.company.errors %}
                  <span>{{error}}</span>
              {% endfor %}
              
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">{{form.mobile.label_tag}}</label>
            {{form.mobile}}
            <div class="text-danger">
              {% for error in form.mobile.errors %}
                  <span>{{error}}</span>
              {% endfor %}
              
            </div>
          </div>
          <div class="mb-3 text-center mt-5">
            <button type="submit" class="btn btn-outline-primary"><i class="bi bi-pencil-square"></i> Update Contact</button>
          </div>
        </form>
      </div>
    </div>
    
  </div>
{% endblock %}

```
