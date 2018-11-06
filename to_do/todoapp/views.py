from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# local imports
from todoapp.models import (Task, UserTask)
from todoapp.forms import UserLoginForm


def get_email_domain(email):
    """A very simple and flawed function to get domain names from a user 
       email"""
    return email.split('@')[1]

def user_login(request):
    """
    Index page of Website. Also serves as a login page.
    """
    user = request.user
    if user.is_authenticated():
        return redirect('home')
    else:
        context = {}
        if request.method == 'POST':
            form = UserLoginForm(request.POST)
            if form.is_valid():
                cred = form.cleaned_data
                user = authenticate(email=cred['email'],
                                    password=cred['password']
                                    )
                if user.is_active:
                    login(request, user)
                    return redirect('home')
        else:
            context["form"] = UserLoginForm()
            return render(request, 'login.html', context)

def home(request):
    user = request.user
    context = {}
    context["user"] = user
    return render(request, 'home.html', context)

def user_register(request):
    """ Register a new user."""

    user = request.user
    if user.is_authenticated():
        return redirect("home")
    context = {}
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            u_name, pwd, user_email= form.save()
            new_user = authenticate(username=user_email, password=pwd)
            login(request, new_user)
            return redirect('home')
        else:
            form = UserRegisterForm()
            return render(request, 'register.html', {'form': form})
