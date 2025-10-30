from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
    cover = models.ImageField(upload_to='course_covers/', null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} — {self.title}"

class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    video_url = models.URLField(blank=True, null=True)   # optional
    is_quiz = models.BooleanField(default=False)

    class Meta:
        unique_together = ('module', 'slug')
        ordering = ['order']

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    user = models.ForeignKey(User, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)
    progress = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} -> {self.course}"

# Contact message model (append to lms/models.py)

class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} — {self.subject}"
