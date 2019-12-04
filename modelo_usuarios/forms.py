from django.db.models import Q
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.template import RequestContext

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
		return authenticate(request, username = self.user.username, password = self.cleaned_data['password'])
		
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
