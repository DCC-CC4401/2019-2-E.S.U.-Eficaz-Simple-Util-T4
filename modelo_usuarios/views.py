from django.shortcuts import render

# Create your views here.

def home_user(request):
	"""
	Logic for the logged account's landing page goes here
	"""
	
	return render(request, "LandingPage_logeado.html")
	
def home_unsigned(request):
	"""
	Logic for the unsigned account's landing page goes here
	"""
	
	return render(request, "LandingPage_nologeados.html")
	
def user_profile(request):
	"""
	Logic for the user profile page goes here
	"""
	
	return render(request, "UserProfile.html")

def user_register(request):
	"""
	Logic for the user register page goes here
	"""

	return render(request, "Registration_page.html")