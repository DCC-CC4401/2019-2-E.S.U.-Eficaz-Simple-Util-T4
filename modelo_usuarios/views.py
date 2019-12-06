from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .forms import LogSession, CustomUserCreationForm
from django.contrib.auth.models import User



# Create your views here.

def home_unsigned(request):
	"""
	Logic for the unsigned account's landing page goes here
	"""
	if request.method == 'POST':
		log_form = LogSession(request.POST)
		if log_form.is_valid():
			user = log_form.authenticate_user(request)
			if user is not None:
				login(request, user)
				return redirect('http://127.0.0.1:8000/home/')
			else:
				log_form = LogSession() 
				#Should raise error in the CSS	
	else:
		log_form = LogSession()
			
	return render(request, "LandingPage_nologeados.html")

def home_user(request):
	"""
	Logic for the logged account's landing page goes here
	"""
	
	
	return render(request, "LandingPage_logeado.html")
	

	
def user_profile(request):
	"""
	Logic for the user profile page goes here
	"""
	
	return render(request, "UserProfile.html")


def user_register(request):
	"""
	Logic for the user register page goes here
	"""
	if request.method == 'POST':
		f = CustomUserCreationForm(request.POST, request.FILES)
		print(f)
		if f.is_valid():
			print('valid')
			f.save()
			return redirect('http://127.0.0.1:8000/home/')
	else:
		print(':c')
		f = CustomUserCreationForm()
	context = {
		'form': f
	}
	return render(request, "Registration_page.html", context)

