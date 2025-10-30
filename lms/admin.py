from django.contrib import admin
from .models import Course, Module, Lesson, Enrollment
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_on', 'handled')
    list_filter = ('handled', 'submitted_on')
    search_fields = ('name', 'email', 'subject', 'message')

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'created')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'is_quiz')
    prepopulated_fields = {'slug': ('title',)}
