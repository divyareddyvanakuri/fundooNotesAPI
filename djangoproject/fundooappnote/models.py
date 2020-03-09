from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Person(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=15)
    confirmpassword = models.CharField(max_length=15)

    def __str__(self):
        return self.username


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    text = models.TextField() 
    archive = models.BooleanField(default=False)