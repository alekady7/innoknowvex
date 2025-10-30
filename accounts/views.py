from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

def register_view(request):
    # if already logged in, send to home
    if request.user.is_authenticated:
        return redirect('lms:home')

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            if email:
                user.email = email
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, "Account created. Please log in.")
            return redirect('accounts:login')
    else:
        form = RegisterForm()

    # reuse the lms signup template you already have
    return render(request, "lms/signup.html", {"form": form})


def login_view(request):
    # if already logged in, go to home
    if request.user.is_authenticated:
        return redirect('lms:home')

    next_url = request.GET.get('next') or request.POST.get('next') or reverse('lms:home')

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(next_url)
    else:
        form = LoginForm()

    # reuse the lms login template you already have
    return render(request, "lms/login.html", {"form": form, "next": next_url})


def logout_view(request):
    # accept both GET and POST — but templates should use POST
    if request.user.is_authenticated:
        logout(request)
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
