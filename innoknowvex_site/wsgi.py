"""
WSGI config for innoknowvex_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.contrib.auth import get_user_model
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innoknowvex_site.settings')

application = get_wsgi_application()

def create_admin_on_startup():
    try:
        from django.db.utils import OperationalError
        User = get_user_model()
        username = os.environ.get("ADMIN_USER", "admin")
        email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
        password = os.environ.get("ADMIN_PW")
        if password:
            user, created = User.objects.get_or_create(username=username, defaults={"email": email})
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
    except OperationalError:
        # DB not ready (migrations not run) - ignore
        pass
    except Exception:
        # swallow to avoid bringing down the app; monitor logs
        import logging
        logging.exception("create_admin_on_startup failed")

create_admin_on_startup()
