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
    path('allRequests/', views.field_requests, name='field_requests'),
    path('addDepartment/', views.add_department, name='add_department'),
    path('addSupervisor/', views.register_supervisor, name='register_supervisor'),
    path('coordinatorDash/', views.coordinatorDash, name='coordinator_Dashboard'),
    path('allStudents/', views.retrieveStudents, name='AllStudents'),
    path('NewRequests/', views.newRequests, name='AllRequestDetails'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('allUsers/', views.retrieve_all_users, name='allUsers'),
    path('allSupervisors/', views.retrieve_all_supervisors, name='allSupervisors'),
    path('allDepartments/', views.retrieve_Departments, name='Departments'),
    path('RepliedRequests/', views.retrieve_replies, name='replies'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('department/<int:department_id>', views.department_details, name='dep_information'),
    path('request/<int:request_id>/', views.approve_or_reject_request, name='decision'),
    path('departmentDetails/', views.department_list, name='D_information'),
]