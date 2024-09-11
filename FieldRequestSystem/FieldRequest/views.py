from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.utils import timezone
from datetime import date
from django.contrib.auth import get_user_model

def landing_page(request):
    return render(request, 'landing_page.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['fullname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.add_message(request, messages.ERROR,"Passwords do not match!", extra_tags='danger')
            return redirect('register')
        if CustomUser.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,"Username already taken", extra_tags='danger')
        if CustomUser.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, "Username in use", extra_tags='danger')
            return redirect('register')
        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        user.is_student = True
        user.save()
        
        return redirect('login')
    return render(request, 'Studentregister.html')

#LoginView
def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect("student_dashboard")
        elif request.user.is_supervisor:
            return redirect("coordinator_Dashboard")
    
    if request.method == 'POST':
        username = request.POST['fullname']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_student:
                return redirect('student_dashboard')
            elif user.is_supervisor:
                return redirect('coordinator_Dashboard')
        else:
            messages.add_message(request, messages.ERROR,"Invalid username or password",extra_tags='danger')
            return redirect('login')
    
    return render(request, 'Login.html')


#Additional Student Details
@login_required
def Student_details(request):
     if request.method == 'POST':
        student = CustomUser.objects.get(id=request.user.id)  
        profile_pic = request.FILES['profilePic']
        age = request.POST['age']
        university = request.POST['university']
        course = request.POST['course']
        year = request.POST['year']
        try:    
            student_details = StudentDetails(
                student=student,
                profilePic=profile_pic,
                age=age,
                university=university,
                course=course,
                year=year
            )
            student_details.save()
        except IntegrityError:
            messages.info(request, 'Student Does Not exist!!!!')
            return redirect('add_student_details') 
        messages.success(request, 'Student Details Successfully Added!!')
        return redirect('student_dashboard')   
    
     return render(request, 'studentInfo.html')
 
#Request for Field View
@login_required
def request_field_training(request):
    Deps=Department.objects.all()
    context = {
        'Deps': Deps,
    }
    if request.method == 'POST':
        current_user = request.user

        # Retrieve the StudentDetails instance for the logged-in user
        try:
            student_details = StudentDetails.objects.get(student=current_user)
        except StudentDetails.DoesNotExist:
            # Handle the case where there is no StudentDetails for the user
            messages.add_message(request, messages.ERROR, 'No student details found. Please complete your profile first.', extra_tags='danger')
            return redirect('add_student_details')
        
        department = request.POST['department']
        region = request.POST['region']
        application_letter = request.FILES['applicationLetter']
        description = request.POST['description']
        startDate  = request.POST['start-date']
        endDate  = request.POST['end-date']
        
        startDate = date.fromisoformat(startDate)
        endDate = date.fromisoformat(endDate)
        today = date.today()
        
        if startDate < today:
            messages.add_message(request, messages.ERROR, "The start date cannot be in the past.", extra_tags='danger')
            return render(request, 'RequestDetails.html',context) 
        
        if endDate < startDate:
           messages.add_message(request, messages.ERROR, "The end date cannot be before the start date.", extra_tags='danger')
           return render(request, 'RequestDetails.html',context)  

        request_details = RequestDetails(
            s_details=student_details,
            department=department,
            region=region,
            applicationLetter=application_letter,
            description=description,
            startDate=startDate,
            endDate=endDate
        )
        request_details.save()
        messages.success(request, 'Request submitted successfully!')
        return redirect('request_field_training') 
    else:
        return render(request, 'RequestDetails.html',context) 
    
#Field request status
@login_required    
def Request_status(request):
    user = request.user
    
    Srequests = RequestDetails.objects.none()
    
    try:
        student_details = StudentDetails.objects.get(student=user)
        Srequests = RequestDetails.objects.filter(s_details=student_details)
    except StudentDetails.DoesNotExist:
        pass
        
    contextt = {
        'user': user,
        'Srequests': Srequests,
    }
    
    return render(request, 'Status.html', contextt) 
 
#LogOut View  
@login_required  
def user_logout(request):
    logout(request)
    return redirect('login') 




@login_required
def student_dashboard(request):
    # Get the logged-in user
    user = request.user

    # Try to retrieve the associated student details
    try:
        studentDetails = StudentDetails.objects.get(student=user)
    except StudentDetails.DoesNotExist:
        studentDetails = None

    context = {
        'user': user,
        'studentDetails': studentDetails,
    }

    return render(request, 'dashboard.html', context)


User=get_user_model()
@login_required
def field_requests(request):
    # Fetch all field requests
    Srequests = RequestDetails.objects.select_related('s_details').all()
    context = {
        'Srequests': Srequests,
    }
    return render(request, 'allRequests.html', context)


@login_required
def add_department(request):
    if request.method == 'POST':
        name = request.POST['deptName']
        location = request.POST['location']
        hod = request.POST['hod']
        email = request.POST['email']
        contact = request.POST['contact']
        description = request.POST['description']

        # Create a new Department
        department = Department.objects.create(
            name=name,
            location=location,
            head_of_department=hod,
            email=email,
            contact=contact,
            description=description
        )
        department.save()
        messages.success(request, 'Department added successfully.')
        return redirect('add_department')
    
    return render(request, 'addDepartment.html')


@login_required
def register_supervisor(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        contact = request.POST['contact']
        profile_pic = request.FILES.get('profilePic')

        if password1 != password2:
            messages.add_message(request, messages.ERROR,"Passwords do not match.", extra_tags='danger')
            return redirect('register_supervisor')
        if CustomUser.objects.filter(username=fullname).exists():
           messages.add_message(request, messages.ERROR, "Username already taken!!", extra_tags='danger')
        if CustomUser.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, "Email already taken!!", extra_tags='danger')
            return redirect('register_supervisor')

        # Create a new user and supervisor
        user = User.objects.create_user(username=fullname, email=email, password=password1)
        user.is_supervisor = True
        user.save()

        supervisor = Supervisor.objects.create(user=user, contact=contact, profilePic=profile_pic)
        supervisor.save()

        messages.success(request, 'Supervisor registered successfully.')
        return redirect('register_supervisor')

    return render(request, 'addSupervisor.html')


@login_required
def retrieveStudents(request):
    # Try to retrieve the associated student details
    allstudents=StudentDetails.objects.select_related('student').all()
    content = {
        'allstudents' : allstudents,
    }

    return render(request, 'allStudents.html', content)


@login_required
def coordinatorDash(request):
         # Total number of users
    total_users = CustomUser.objects.count()
    
    # Total number of students
    total_students = StudentDetails.objects.count()
    
    # Total number of supervisors
    total_supervisors = Supervisor.objects.count()
    
    # Total number of departments
    total_departments = Department.objects.count()
    
    # Total number of requests
    total_requests = RequestDetails.objects.count()
    
    # Total number of new requests (with no coordinator_response or coordinator_response is None)
    new_requests = RequestDetails.objects.filter(coordinator_response__isnull=True).count()

    context = {
        'total_users': total_users,
        'total_students': total_students,
        'total_supervisors': total_supervisors,
        'total_departments': total_departments,
        'total_requests': total_requests,
        'new_requests': new_requests,
    }
     
    return render(request, 'coordinatorDash.html', context)
 
 
@login_required
def allRequestDetails(request):
    
     return render(request, 'MoreDetails.html')
 

@login_required
def student_detail(request, student_id):
    student = get_object_or_404(StudentDetails, id=student_id)
    
    context = {
        'student': student,
    }
    return render(request, 'student_detail.html', context)


@login_required
def retrieve_all_users(request):
    people=CustomUser.objects.all()
    
    context = {
        'people' : people,
         
    }
    return render(request, 'allUsers.html', context)


@login_required
def retrieve_all_supervisors(request):
    instructors=Supervisor.objects.select_related('user').all()
    context = {
        'instructors' : instructors,
    }
    return render(request, 'allSupervisors.html', context)

@login_required
def newRequests(request):
    Nrequests = RequestDetails.objects.filter(coordinator_response__isnull=True).all()
    
    context = {
        'Nrequests' : Nrequests,
    }
    return render(request, 'NewRequests.html', context)

@login_required
def retrieve_Departments(request):
    Deps=Department.objects.all()
    
    context = {
        'Deps' : Deps,
    }
    return render(request, 'allDepartments.html', context)

@login_required
def retrieve_replies(request):
    Nrequests = RequestDetails.objects.filter(coordinator_response__isnull=False).all()
    
    context = {
        'Nrequests' : Nrequests,
    }
    return render(request, 'RepliedRequests.html', context)


@login_required
def user_detail(request, user_id):
    student = get_object_or_404(CustomUser, id=user_id)
    
    context = {
        'student': student,
    }
    return render(request, 'userDetails.html', context)

@login_required
def department_details(request, department_id):
    deps = get_object_or_404(Department, id=department_id)
    
    context = {
        'deps': deps,
    }
    return render(request, 'departmentDetail.html', context)


@login_required
def request_view(request,request_id):
    applications = get_object_or_404(RequestDetails,id=request_id)
    
    context = {
        'applications' : applications,
    }
    return render(request, 'R_decision.html', context)

@login_required
def approve_or_reject_request(request, request_id):
    req = get_object_or_404(RequestDetails, id=request_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            req.coordinator_response = 'Approved'
        elif action == 'reject':
            req.coordinator_response = 'Rejected'
        req.save()
        return redirect('field_requests')  

    return render(request, 'R_Decision.html', {'request_detail': req})


@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departmentDetails.html', {'departments': departments})