from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    '''
    Profile fields
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE) # username, password, email, first_name, last_name
    tiempo_conexion = models.DateField(auto_now=True)


class Category(models.Model):
    '''
    Category fields

    A category belongs to a user

    A category table must exist to avoid non wanted behavior like category=Correr, category=corriendo, ... have only 1 category
    '''
    category = models.CharField(max_length=150)


class Activity(models.Model):
    '''
    Activity fields
    '''
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Category)
    date = models.DateField(auto_now=True)
    start_time = models.TimeField(auto_now=True)
    end_time = models.TimeField() # duracion = end-start!

class ActivityTemplate(models.Model):
    '''
    A template for a kind of activity

    A category belongs to a user ==> template belongs to a user
    '''
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Friend(models.Model):
    '''
    A friend of the user

    He's also an user
    '''
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    friend = models.ForeignKey(Profile, on_delete=models.CASCADE)
