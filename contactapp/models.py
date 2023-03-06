from django.db import models

# Create your models here.
class Contact(models.Model):
  firstname = models.CharField(max_length=20)
  lastname = models.CharField(max_length=20)
  company = models.CharField(max_length=20)
  mobile = models.CharField(max_length=10)

  def __str__(self):
    return self.firstname