from django.db import models
from django.contrib.auth.models import User

class students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    age = models.IntegerField()
    
    
class StudentDetails(models.Model):
    applicant = models.ForeignKey(students, on_delete=models.CASCADE)
    profilePic = models.ImageField()
    university = models.CharField(max_length=100)
    course = models.CharField(max_length=150)
    year = models.IntegerField()
    
    
class RequestDetails(models.Model):
    s_details = models.ForeignKey(students , on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    applicationLetter = models.FileField()
    description = models.CharField(max_length=500)

# Create your models here.
