from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .forms import LogSession

# Create your views here.

def home_unsigned(request):
	"""
	Logic for the unsigned account's landing page goes here
	"""
	print("Hi")
	if request.method == 'POST':
		print("Step_A passed")
		log_form = LogSession(request.POST)
		if log_form.is_valid():
			print("Step_B passed")
			p_email = log_form.cleaned_data['email']
			p_password = log_form.cleaned_data['password']
			#print(p_email)
			#print(p_password)
			user = authenticate(request, email = p_email, password = p_pass)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect('/thanks/')
			else:
				raise Http404 
				#Should raise error in the CSS
		else:
			print("Failed")
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