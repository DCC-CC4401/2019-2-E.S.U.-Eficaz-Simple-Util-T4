from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import Profile



# Forms used go here

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


class CustomUserCreationForm(forms.Form):
    first_name = forms.CharField(label='Enter first name',  max_length=256, widget=forms.TextInput(attrs={'class' : 'myfieldclass'}))
    last_name = forms.CharField(label='Enter last name', max_length=256)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    profilePicture = forms.ImageField(label='imagen de usuario', required=False)
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        return last_name

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def clean_image(self):
        image = self.cleaned_data.get('profilePicture')
        return image

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.clean_email(),
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        profile = Profile.objects.create(user=user, profile_photo=self.cleaned_data['profilePicture'])
        profile.save()
        return user

class ChangeAvatar(forms.Form):
	photo = forms.ImageField(label='', required=False, widget=forms.ClearableFileInput(
		attrs={
			'id': 'files',
			'onchange': 'this.form.submit()'}
	))

class changePass(forms.Form):
	old_pass = forms.CharField(label='Contraseña actual', widget=forms.PasswordInput(
		attrs={'class': 'form_control',
			   'placeholder': "************"}
	))
	new_pass = forms.CharField(label='Contraseña nueva', widget=forms.PasswordInput(
		attrs={'class': 'form_control',
			   'placeholder': "ingrese contraseña"}
	))
	confirm_pass = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(
		attrs={'class': 'form_control',
			   'placeholder': "repita contraseña"}
	))
