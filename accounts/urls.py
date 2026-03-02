from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.user_login, name='home'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
]