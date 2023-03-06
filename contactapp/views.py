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