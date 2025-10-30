# lms/utils.py
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect

def is_instructor(user):
    return user.is_staff or user.groups.filter(name='instructor').exists()

def instructor_required(view_func):
    """
    Decorator for views that require the user to be an instructor (staff or in 'instructor' group).
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('lms:login')
        if not is_instructor(request.user):
            return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
