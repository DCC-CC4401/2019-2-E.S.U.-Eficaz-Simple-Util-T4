from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user
from django.db.models.signals import post_save
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.staticfiles.templatetags.staticfiles import static
from .forms import LogSession
from .forms import ChangeAvatar
from .forms import changePass

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
		img_path = 'http://127.0.0.1:8000/'+'profile_photo/'+str(profile.profile_photo)


	if request.method == 'POST':
		formp = ChangeAvatar(request.POST, request.FILES)
		passform = changePass(request.POST)

		if passform.is_valid():
			oldp = passform.cleaned_data['old_pass']
			newp = passform.cleaned_data['new_pass']
			conp = passform.cleaned_data['confirm_pass']
			username = request.user.username
			user = authenticate(request, username = username, password = oldp)
			if user is not None and oldp and newp and conp and newp == conp:
				user.set_password(newp)
				user.save()
				return HttpResponseRedirect('http://127.0.0.1:8000')

		if formp.is_valid():
			(us, created) = Profile.objects.get_or_create(user=get_user(request))
			us.profile_photo = formp.cleaned_data['photo']
			us.save()
			return HttpResponseRedirect('http://127.0.0.1:8000/profile')


	formp = ChangeAvatar()
	passform = changePass()
	context = {'username': current.username,
			   'first_name': current.first_name,
			   'last_name': current.last_name,
			   'email': current.email,
			   'img_src': img_path,
			   'formp': formp,
			   'passform' : passform
			   }
	return render(request, "UserProfile.html", context)
	
def user_register(request):
	"""
	Logic for the user register page goes here
	"""

	return render(request, "Registration_page.html")