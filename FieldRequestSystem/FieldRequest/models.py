from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
   
class StudentDetails(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='studentdetails')
    profilePic = models.ImageField(upload_to='profile_pics/')
    age = models.IntegerField()
    university = models.CharField(max_length=100)
    course = models.CharField(max_length=150)
    year = models.IntegerField()

    def __str__(self):
        return self.student.username    

class RequestDetails(models.Model):
    s_details = models.ForeignKey(StudentDetails, on_delete=models.CASCADE, related_name='requests')
    department = models.CharField(max_length=100)
    applicationLetter = models.FileField(upload_to='application_letters/')
    description = models.CharField(max_length=500)
    startDate = models.DateField(default=timezone.now)
    endDate = models.DateField(default=timezone.now)
    coordinator_response = models.CharField(max_length=10, choices=[('Approved', 'Approved'), ('Rejected', 'Rejected')], null=True, blank=True) 

    def __str__(self):
        return f"{self.s_details.username} - {self.department}"

