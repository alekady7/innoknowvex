import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innoknowvex_site.settings')

application = get_wsgi_application()

def _create_admin_on_startup():
    """
    Optional: create/update a superuser on startup.
    Only runs if AUTO_CREATE_ADMIN env var is set to "true".
    Requires ADMIN_USER and ADMIN_PW env vars to be present.
    WARNING: keep AUTO_CREATE_ADMIN off in production after initial use.
    """
    try:
        if os.environ.get("AUTO_CREATE_ADMIN", "false").lower() != "true":
            return

        # read env (do NOT hardcode defaults with passwords)
        username = os.environ.get("ADMIN_USER")
        email = os.environ.get("ADMIN_EMAIL", "")
        password = os.environ.get("ADMIN_PW")

        if not username or not password:
            logging.warning("AUTO_CREATE_ADMIN enabled but ADMIN_USER or ADMIN_PW missing; skipping admin creation.")
            return

        # Imported here to avoid using auth before Django is fully configured
        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )
        # If exists, make sure flags and password are set/updated
        if not user.is_staff or not user.is_superuser:
            user.is_staff = True
            user.is_superuser = True
        # Always set password to the env one (use caution)
        user.set_password(password)
        user.email = email or user.email
        user.save()

        logging.info(f"{'Created' if created else 'Updated'} admin user '{username}' on startup.")
    except OperationalError:
        # DB not yet ready (migrations), safe to ignore here
        logging.warning("Database not ready; skipping admin creation.")
    except Exception:
        logging.exception("Admin creation on startup failed (see stacktrace).")

# run the creation (guarded)
_create_admin_on_startup()
