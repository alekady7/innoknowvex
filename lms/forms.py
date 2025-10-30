from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import ContactMessage

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'subject', 'message')
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6}),
        }
