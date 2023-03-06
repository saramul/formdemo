from django.db import models

# Create your models here.
class Person(models.Model):
  firstname = models.CharField(max_length=30)
  lastname = models.CharField(max_length=30)
  email = models.EmailField(max_length=100)
  phone = models.CharField(max_length=20)
  bio = models.TextField(max_length=500)

  def __str__(self):
    return self.firstname