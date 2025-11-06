from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.db.models import Q
from django.views.decorators.http import require_POST

from .models import Profile
from .forms import StaffUserCreateForm, StaffUserUpdateForm

User = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        return redirect('lms:home')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect(request.POST.get('next') or 'lms:home')
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('lms:home')
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('lms:home')
    return render(request, 'accounts/register.html', {'form': form})

@login_required(login_url='accounts:login')
@require_POST
def logout_view(request):
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


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'accounts:login'
    def test_func(self):
        return self.request.user.is_staff


class StaffUserListView(StaffRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 30

    def get_queryset(self):
        qs = User.objects.all().select_related('profile').order_by('-date_joined')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(username__icontains=q) |
                Q(email__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(profile__phone__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class StaffUserCreateView(StaffRequiredMixin, CreateView):
    model = User
    form_class = StaffUserCreateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:staff_user_list')

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


class StaffUserUpdateView(StaffRequiredMixin, UpdateView):
    model = User
    form_class = StaffUserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:staff_user_list')

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs.get('pk'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        profile, _ = Profile.objects.get_or_create(user=self.get_object())
        kwargs['profile'] = profile
        return kwargs

    def form_valid(self, form):
        user = form.save()
        # Save profile fields if present in form.cleaned_data
        profile = Profile.objects.get(user=user)
        # form may include role/phone/title fields (your form controls this)
        if 'role' in form.cleaned_data:
            profile.role = form.cleaned_data.get('role')
        if 'phone' in form.cleaned_data:
            profile.phone = form.cleaned_data.get('phone', '')
        if 'title' in form.cleaned_data:
            profile.title = form.cleaned_data.get('title', '')
        profile.save()
        return redirect(self.success_url)


class StaffUserDetailView(StaffRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_obj'

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs.get('pk'))
