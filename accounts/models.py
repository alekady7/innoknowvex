# accounts/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

User = get_user_model()

class Profile(models.Model):
    ROLE_STUDENT = 'student'
    ROLE_EMPLOYEE = 'employee'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
        (ROLE_STUDENT, 'Student'),
        (ROLE_EMPLOYEE, 'Employee'),
        (ROLE_ADMIN, 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default=ROLE_STUDENT)
    phone = models.CharField(max_length=40, blank=True, null=True)
    title = models.CharField(max_length=120, blank=True, null=True)
    avatar_url = models.CharField(max_length=512, blank=True, null=True)  # optional if you add uploads later

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile: {self.user.username} ({self.role})"

# auto-create Profile when User is created
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
