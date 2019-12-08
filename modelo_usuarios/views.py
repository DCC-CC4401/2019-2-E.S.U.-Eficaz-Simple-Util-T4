from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from modelo_usuarios import forms
from modelo_usuarios.models import Profile


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

@login_required()
def update_profile_photo(request):
	try:
		user_profile = Profile.objects.get(user=request.user)
	except Profile.DoesNotExist:
		return HttpResponse("Perfil de usuario incorrecto!")

	if request.method == "POST":
		form = forms.PhotoForm(request.POST, request.FILES)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.user = request.user
			profile.save()
			return redirect("UserProfile.html")
	else:
		form = forms.PhotoForm()
	return render(request, 'UserProfile.html', {'form': form})
