from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('Studentregister/', views.register, name='register'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('studentInfo/', views.Student_details, name='add_student_details'),
    path('RequestDetails/', views.request_field_training, name='request_field_training'),
    path('Status/', views.Request_status, name='request_Status'), 
]