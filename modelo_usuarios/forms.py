from django import forms
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
