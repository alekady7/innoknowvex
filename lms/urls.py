from django.urls import path
from . import views

app_name = 'lms'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('lesson/<course_slug>/<module_slug>/<lesson_slug>/', views.LessonDetailView.as_view(), name='lesson_detail'),

    path('enroll/<slug:course_slug>/', views.enroll_course, name='enroll_course'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
