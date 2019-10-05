from django.shortcuts import render

# Create your views here.

def home_user(request):
	"""
	Landing Page for logged accounts //Placeholder
	"""
	return render(request, "LandingPage_logeado.html")
	