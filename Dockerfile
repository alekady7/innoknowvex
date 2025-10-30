# ./Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps (kept small)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# copy project into the image
COPY . /app

# expose port
EXPOSE 8000

# default command: run migrations and start development server
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput || true && python manage.py runserver 0.0.0.0:8000"]
