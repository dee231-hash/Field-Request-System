from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.utils import timezone

def landing_page(request):
    return render(request, 'landing_page.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['fullname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Username in use")
            return redirect('register')
        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        user.is_guest = True
        user.save()
        
        return redirect('login')
    return render(request, 'Studentregister.html')

#LoginView
def user_login(request):
    if request.user.is_authenticated:
        return redirect("student_dashboard")
    if request.method == 'POST':
        username = request.POST['fullname']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid username or password")
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
    if request.method == 'POST':
        s_details = request.user
        department = request.POST['department']
        application_letter = request.FILES['applicationLetter']
        description = request.POST['description']
        startDate  = request.POST['start-date']
        endDate  = request.POST['end-date']

        request_details = RequestDetails(
            s_details=s_details,
            department=department,
            applicationLetter=application_letter,
            description=description,
            startDate=startDate,
            endDate=endDate
        )
        request_details.save()
        messages.success(request, 'Request submitted successfully!')
        return redirect('student_dashboard') 
    else:
        return render(request, 'RequestDetails.html') 
    
#Field request status
@login_required    
def Request_status(request):
     student_requests = StudentDetails.objects.filter(student=request.user)

     return render(request, 'Status.html', {'request_Status': student_requests}) 
 
#LogOut View  
@login_required  
def user_logout(request):
    logout(request)
    return redirect('login') 


@login_required
def student_dashboard(request):
    if not request.user.is_authenticated or not CustomUser.objects.filter(id=request.user.id).exists():
        messages.error(request, 'You do not have access to this page.')
        return redirect('login')

    return render(request, 'dashboard.html')


