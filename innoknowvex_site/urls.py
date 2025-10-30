from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # accounts first so /login resolves to accounts
    path('', include('accounts.urls')),

    # LMS app handles home and site pages
    path('', include('lms.urls')),
]
