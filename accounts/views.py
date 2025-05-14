from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .utils import get_otp
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from movies.models import movies

# Create your views here.


def registerview(request):
    fm =   RegisterForm()
    context = {
        'registerform': fm
    }
    if request.method == 'POST':
        user = RegisterForm(request.POST)
        if user.is_valid():
           
            user.save()
            username = user.cleaned_data['username']
            email = user.cleaned_data['email']
            send_mail (
                'Registration Successful',
                f'{username} You have successfully registered in MOvie Booking App.',
                'vishnunandanar901@gmail.com',
                [email],
                fail_silently=True

            )
            messages.success(request, 'You have Created an Account successfully')
            return redirect('login')
    return render(request, 'accounts/register.html', context)


def loginviews(request):
    fm=AuthenticationForm()
    context={
        'form':fm
    }
    if request.method =='POST':
        fm=AuthenticationForm(data=request.POST)
        if fm.is_valid():
            username = fm.cleaned_data['username']
            password = fm.cleaned_data['password']
            user_object=authenticate(username=username, password=password)
            if user_object is not None:
                if user_object.is_authenticated:
                    login(request, user_object)
                    messages.success(request, 'You are logged in Successfully')
                    return redirect('home')
            return HttpResponse('invalid username or password')
    return render(request, 'accounts/login.html', context)  

def logoutview(request):
    logout(request)
    messages.error(request, 'Logged out Successfully')
    return redirect('login')

@login_required(login_url='/login/')
def homeview(request):
    all_movies = movies.objects.all()
    return render(request, 'accounts/home.html', {'movies': all_movies})
