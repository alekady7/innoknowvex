# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.urls import reverse
import os
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_GET
from django.conf import settings
from django.contrib.auth import get_user_model

@require_GET
def create_superuser_via_token(request, token):
    """
    Temporary endpoint to create/update a superuser.
    Protected by CREATE_SUPERUSER_TOKEN env var.
    WARNING: Remove this view and URL immediately after use.
    """
    secret = os.environ.get('CREATE_SUPERUSER_TOKEN')
    if not secret:
        return HttpResponseForbidden("CREATE_SUPERUSER_TOKEN not set on server.")

    if token != secret:
        return HttpResponseForbidden("Invalid token.")

    # get admin credentials from env (fall back to defaults)
    username = os.environ.get('ADMIN_USER', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    password = os.environ.get('ADMIN_PW')

    if not password:
        return HttpResponse("ADMIN_PW not set on server. Set it then retry.", status=400)

    User = get_user_model()
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save()

    return HttpResponse(f"{'Created' if created else 'Updated'} superuser '{username}'. Please DELETE this endpoint now.", status=200)


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
