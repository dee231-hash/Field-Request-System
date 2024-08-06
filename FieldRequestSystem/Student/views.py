from django.shortcuts import render , redirect
from django.contrib.auth import login
from .models import students, RequestDetails, StudentDetails


def Login_student(request):
    if request.method == 'POST':
        username = request.POST

# Create your views here.
