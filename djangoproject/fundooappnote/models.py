from django.db import models

# Create your models here.
class Person(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=15)
    confirmpassword = models.CharField(max_length=15)
