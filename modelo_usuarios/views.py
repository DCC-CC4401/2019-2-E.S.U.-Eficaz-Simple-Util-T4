from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user
from django.shortcuts import redirect

from django.contrib.staticfiles.templatetags.staticfiles import static
from .forms import LogSession
from .forms import ChangeAvatar

from django.contrib import messages
from django.contrib.auth.models import User


from .models import Profile


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
	##Test this by connecting through "jalmarza@gmail.com"/"real_human" user
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

	return render(request, "Registration_page.html")

def new_photo(request):
	if request.method == 'POST':
		formp = ChangeAvatar(request.POST, request.FILES)
		if formp.is_valid():
			(newph, created) = User.objects.get_or_create(user=get_user(request))
			newph.image = formp.cleaned_data['photo']
			newph.save()
			messages.success(request, '¡se modificó su foto de perfil exitosamente!')
			return render(request, "UserProfile.html", {'formp': formp})
		messages.warning(
			request,
			'Error, reintentelo'
		)
	return render(request, "UserProfile.html", {'formp': formp})



