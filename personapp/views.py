from django.shortcuts import render, redirect
from .models import Person
from .forms import PersonForm
from django.contrib import messages

# Create your views here.
def show_all(request):
  persons = Person.objects.all()
  context = {
    'title':'Show All Persons',
    'persons': persons
  }
  return render(request, 'person/show_all.html', context) 

def new_person(request):
  if request.method == 'POST':
    form = PersonForm(request.POST)
    if form.is_valid():
      person = form.save(commit=True)
      person.save()

      messages.success(request, 'Add New Person Successfully!')
      return redirect(to='personapp:show_all')
  else:
    form = PersonForm()

  context = {
    'title': 'Add New Person',
    'form': form
  }
  return render(request, 'person/new_person.html', context)

def update_person(request, id):
  person = Person.objects.get(id=id)

  if request.method == 'POST':
    form = PersonForm(request.POST, instance=person)
    if form.is_valid():
      person = form.save(commit=True)
      person.save()
      messages.success(request, 'Update Person Successfully!')
      return redirect(to='personapp:show_all')
  else:
    form = PersonForm(instance=person)

  context = {
    'title':'Update Person',
    'form': form
  }
  return render(request, 'person/update_person.html', context)

