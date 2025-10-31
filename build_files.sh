#!/usr/bin/env bash
# build_files.sh — run by Vercel during build
set -e

# install dependencies (optional if Vercel uses requirements.txt automatically)
pip install -r requirements.txt

# collect static files into STATIC_ROOT
python manage.py collectstatic --noinput

python manage.py migrate