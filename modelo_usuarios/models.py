from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, StdDev

# Create your models here.

'''
Usuario (#correo, nombre, apellido, foto, contraseña, rol, tiempo conexión)

Actividades (#U.correo, nombre, descripción, categoría, fecha, hora inicio, duración)

Templates (#U.correo, nombre, descripción, categoría)

Amigos (#U.correo, correo_amigo)

Estadísticas (#U.correo, #categoría, tiempo, desviación estándar)
'''


def profile_photo_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/photo/user_<id>/<filename>
    return 'profile_photo/user_{0}/{1}'.format(instance.usuario.id, filename)

class Profile(models.Model):
    '''
    Profile fields
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # username, password, email, first_name, last_name
    profile_photo = models.ImageField(upload_to=profile_photo_path, null=False)
    # tiempo_conexion = models.DateField(auto_now=True)  ---> está implementado en DJANGO


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
    start_time = models.TimeField(auto_now_add=True)
    end_time = models.TimeField(blank=True)
    lasted = end_time - start_time


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


class Stats(models.Model):
    '''
    Some statistics for the activities of the user
    '''
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # on_delete= cascade??

    def mean_time(self):
        return Activity.objects.all().filter(category=self.category).aggregate(Avg('lasted'))

    def std(self):
        return Activity.objects.all().filter(category=self.category).aggregate(StdDev('lasted'))





