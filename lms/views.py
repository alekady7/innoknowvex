from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Course, Module, Lesson, Enrollment
from .forms import ContactForm

# HomeView redirects unauthenticated visitors to accounts:login
class HomeView(TemplateView):
    template_name = 'lms/home.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy('accounts:login'))
        return super().dispatch(request, *args, **kwargs)


class CourseListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('accounts:login')
    model = Course
    template_name = 'lms/course_list.html'
    context_object_name = 'courses'
    queryset = Course.objects.filter(published=True)


class CourseDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('accounts:login')
    model = Course
    template_name = 'lms/course_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        course = self.object
        user = self.request.user
        ctx['is_enrolled'] = Enrollment.objects.filter(user=user, course=course).exists()
        return ctx


class LessonDetailView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'lms/lesson_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        course_slug = self.kwargs.get('course_slug')
        module_slug = self.kwargs.get('module_slug')
        lesson_slug = self.kwargs.get('lesson_slug')

        lesson = get_object_or_404(
            Lesson,
            slug=lesson_slug,
            module__slug=module_slug,
            module__course__slug=course_slug
        )
        ctx['lesson'] = lesson

        user = self.request.user
        ctx['forbidden'] = not Enrollment.objects.filter(user=user, course=lesson.module.course).exists()
        return ctx


@login_required(login_url=reverse_lazy('accounts:login'))
def enroll_course(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    messages.success(request, f"You are now enrolled in {course.title}.")
    return redirect('lms:course_detail', slug=course_slug)


# Contact form view
class ContactView(FormView):
    template_name = 'lms/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('lms:contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thanks — your message has been received. We'll get back to you soon.")
        return super().form_valid(form)
