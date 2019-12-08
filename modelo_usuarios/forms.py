# Forms used go here
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import filesizeformat

from modelo_usuarios import models
from proyecto_ESU import settings


class PhotoForm(forms.Form):
    class Meta:
        model = models.Profile
        fields = 'profile_photo'

    def clean_photo(self):
        photo = self.cleaned_data.get('photo_profile')
        photo_type = photo.content_type.split('/')[0]
        if photo_type in settings.CONTENT_TYPES:
            if photo.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(
                    'La foto debe tener un tamaño menor a %sMb. El archivo que proporcionó es de %s' % (
                        filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(photo._size)))
        else:
            raise forms.ValidationError('El tipo de archivo es incorrecto')
        return photo


class LogSession(forms.Form):
    email = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)

    def clean(self):
        user = self.authenticate_email()
        if not user:
            raise forms.ValidationError("Error, usuario no encontrado")
        else:
            self.user = user

        return self.cleaned_data

    def authenticate_user(self, request):
        return authenticate(request, username=self.user.username, password=self.cleaned_data['password'])

    def authenticate_email(self):
        email = self.cleaned_data['email']
        if email:
            try:
                user = User.objects.get(email__iexact=email)
                if user.check_password(self.cleaned_data['password']):
                    return user
            except ObjectDoesNotExist:
                pass
        return None
