from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import CustomUserCreationForm
from .models import Profile
from django.contrib.staticfiles.templatetags.staticfiles import static
from .forms import LogSession

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
	current = request.user
	profile = Profile.objects.filter(user = current)[0]	#Obtain user profile
	
	if not profile.profile_photo:	#Empty Image Field, loads default sprite
		img_path = static("img/avatar.png")
	else:
		img_path = static(profile.profile_photo.path)

	context = {'username': current.username,
			 'first_name': current.first_name,
			 'last_name': current.last_name,
			 'email': current.email,
			 'img_src': img_path
			 }

	return render(request, "UserProfile.html", context)


def user_register(request):
	"""
	Logic for the user register page goes here
	"""
	if request.method == 'POST':
		f = CustomUserCreationForm(request.POST, request.FILES)
		if f.is_valid():
			f.save()
			return render(request, "Successful_registration.html")
	else:
		f = CustomUserCreationForm()
	context = {
		'form': f
	}
	return render(request, "Registration_page.html", context)
