from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.user_login, name='home'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('post-job/', views.post_job, name='post_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('job/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),
    path('application/<int:app_id>/<str:status>/',views.update_application_status,name='update_application_status'),
    path('shortlist/<int:application_id>/', views.shortlist_student, name='shortlist_student'),
    path('reject/<int:application_id>/', views.reject_student, name='reject_student'),
    
    
]