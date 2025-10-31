# api/wsgi.py
# Minimal WSGI adapter for serverless hosts (Vercel) or other wrappers.
# Placing this file under `api/` makes it easy for Vercel or other runtimes to import.

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innoknowvex_site.settings')

application = get_wsgi_application()
