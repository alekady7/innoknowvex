# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.urls import reverse

def login_view(request):
    # If already logged in, send to home
    if request.user.is_authenticated:
        return redirect('lms:home')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # After successful login send to home
            return redirect('lms:home')
        else:
            messages.error(request, "Invalid username/password.")
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    # If you want to restrict registration, you can add a check here.
    # Currently it will allow registration; change as desired.
    if request.user.is_authenticated:
        return redirect('lms:home')

    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('lms:home')
        else:
            messages.error(request, "Please correct the errors below.")
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    # After logout send to login page (clean /login)
    return redirect('accounts:login')

@login_required(login_url='accounts:login')
def profile_view(request):
    user = request.user
    first = user.first_name or ""
    last = user.last_name or ""
    initials = (first[:1] + last[:1]).upper()
    context = {
        "first_name": first,
        "last_name": last,
        "initials": initials,
        "user": user,
    }
    return render(request, "accounts/profile.html", context)
