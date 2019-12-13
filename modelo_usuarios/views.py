from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import redirect
from django.shortcuts import render

# Create your views here.
from modelo_usuarios import forms
from modelo_usuarios.models import Profile
from .forms import LogSession


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
            # Should raise error in the CSS
    else:
        log_form = LogSession()

    return render(request, "LandingPage_nologeados.html")


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


def home_unsigned(request):
    """
	Logic for the unsigned account's landing page goes here
	"""

    return render(request, "LandingPage_nologeados.html")


def user_profile(request):
    """
	Logic for the user profile page goes here
	"""
    ##Test this by connecting through "jalmarza@gmail.com"/"real_human" user
    current = request.user
    profile = Profile.objects.filter(user=current)[0]  # Obtain user profile

    if not profile.profile_photo:  # Empty Image Field, loads default sprite
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


@login_required()
def update_profile_photo(request):
    '''
	Logic for updating the profile photo
	'''

    current = request.user
    profile = Profile.objects.filter(user=current)[0]  # Obtain user profile

    if request.method == "POST":
        form = forms.PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            profile = Profile.objects.get(email=request.user)
            profile.profile_photo = request.FILES['imagefile']
            profile.save()
            return redirect("UserProfile.html")
    else:
        form = forms.PhotoForm()
    return render(request, 'UserProfile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'UserProfile.html', {'form': form})
