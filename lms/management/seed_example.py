# quick run in django shell: python manage.py shell
from lms.models import Course, Module, Lesson
c = Course.objects.create(title="Intro to Web Security", slug="intro-web-sec", short_description="Hands-on vulnerabilities and remediation.")
m = Module.objects.create(course=c, title="Basics", order=1)
Lesson.objects.create(module=m, title="What is OWASP?", slug="owasp", content="OWASP overview ...", order=1)
Lesson.objects.create(module=m, title="SQLi basics", slug="sqli", content="SQL injection lab...", order=2)
