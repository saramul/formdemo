from django.urls import path
from . import views

app_name = 'contactapp'
urlpatterns = [
    path('show_all/', views.contacts, name='show_all'),
    path('new_contact/', views.new_contact, name='new_contact'),
    path('<int:id>/update_contact/', views.update_contact, name='update_contact'),
    path('<int:id>/delete_contact/', views.delete_contact, name='delete_contact'),
]