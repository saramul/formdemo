from django.urls import path
from . import views

app_name = 'personapp'
urlpatterns = [
  path('show_all/', views.show_all, name='show_all'),
  path('new_person/', views.new_person, name='new_person'),
  path('<int:id>/update_person/', views.update_person, name='update_person'),
]