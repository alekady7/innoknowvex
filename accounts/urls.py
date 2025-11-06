from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Staff management (admin only)
    path('staff/users/', views.StaffUserListView.as_view(), name='staff_user_list'),
    path('staff/users/add/', views.StaffUserCreateView.as_view(), name='staff_user_add'),
    path('staff/users/<int:pk>/edit/', views.StaffUserUpdateView.as_view(), name='staff_user_edit'),
    path('staff/users/<int:pk>/', views.StaffUserDetailView.as_view(), name='staff_user_detail'),
]
