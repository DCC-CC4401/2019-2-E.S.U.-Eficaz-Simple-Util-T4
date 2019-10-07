from django import forms

# Forms used go here

class LogSession(forms.Form):
	email = forms.CharField(max_length=255)
	password = forms.CharField(max_length=255)