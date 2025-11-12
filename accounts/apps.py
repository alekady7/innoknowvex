from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError
import os
import logging

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        # only run if explicitly allowed (to avoid running during every migration)
        if os.environ.get("AUTO_CREATE_ADMIN", "true").lower() != "true":
            return

        try:
            User = get_user_model()
            username = os.environ.get("ADMIN_USER")
            email = os.environ.get("ADMIN_EMAIL")
            password = os.environ.get("ADMIN_PW")

            if not username or not password:
                logging.warning("Admin creation skipped: missing ADMIN_USER or ADMIN_PW in env.")
                return

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "is_staff": True,
                    "is_superuser": True,
                },
            )
            if created:
                user.set_password(password)
                user.save()
                logging.info(f"Created default admin user '{username}'.")
            else:
                logging.info(f"Admin user '{username}' already exists — skipping creation.")
        except OperationalError:
            logging.warning("Database not ready, skipping admin creation.")
        except Exception as e:
            logging.exception("Failed to auto-create admin user.")
