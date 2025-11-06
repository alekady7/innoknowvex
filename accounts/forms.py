from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="Optional")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

class StaffUserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=False, initial=Profile.ROLE_STUDENT)
    phone = forms.CharField(required=False)
    title = forms.CharField(required=False)
    is_staff = forms.BooleanField(required=False, label='Is staff')
    is_active = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2", "is_staff", "is_active")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '')
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.is_staff = self.cleaned_data.get('is_staff', False)
        user.is_active = self.cleaned_data.get('is_active', True)
        if commit:
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = self.cleaned_data.get('role', Profile.ROLE_STUDENT)
            profile.phone = self.cleaned_data.get('phone', '')
            profile.title = self.cleaned_data.get('title', '')
            profile.save()
        return user

class StaffUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=False)
    phone = forms.CharField(required=False)
    title = forms.CharField(required=False)
    is_staff = forms.BooleanField(required=False)
    is_active = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "is_staff", "is_active")

    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)
        if profile:
            self.fields['role'].initial = profile.role
            self.fields['phone'].initial = profile.phone
            self.fields['title'].initial = profile.title
