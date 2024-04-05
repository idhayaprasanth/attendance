from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone


    
class department(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class staff(models.Model):
    department = models.ForeignKey(department,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    mobile = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f" {self.department.name} - {self.name}"
    

class classroom(models.Model):
    department = models.ForeignKey(department,on_delete=models.CASCADE)
    year_choice = [
        ('1st', '1st'),('2nd','2nd'),('3rd','3rd'),
    ]
    year=models.CharField(max_length=3,choices=year_choice)
    section_choice = [
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('E','E'),
        ('F','F'),
        ('G','G'),
        ('H','H'),
        ('I','I'),
        ('J','J'),
    ]
    section=models.CharField(max_length=1,choices=section_choice)
    subject1 = models.CharField(max_length=100,null=True)
    subject2 = models.CharField(max_length=100,null=True)
    subject3 = models.CharField(max_length=100,null=True)
    subject4 = models.CharField(max_length=100,null=True)
    subject5 = models.CharField(max_length=100,null=True)
    subject6 = models.CharField(max_length=100,null=True)
    subject7 = models.CharField(max_length=100,null=True)
    subject8 = models.CharField(max_length=100,null=True)
    subject9 = models.CharField(max_length=100,null=True)

    def __str__(self):
        return f" {self.year} -{self.section}-{self.department}"
class student_record(models.Model):  
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    classroom = models.ForeignKey(classroom,on_delete=models.CASCADE)
    reg = models.SlugField(max_length=20,unique=True)
    name=models.CharField(max_length=100)
    mobile = models.IntegerField()
    gender_choice = [
        ("male","male"),("female","female"),
    ]
    gender = models.CharField(max_length=6,choices=gender_choice,null=True)


    def __str__(self):
        return f"{self.name}"
class attendance(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=date.today)
    classroom = models.ForeignKey(classroom, on_delete=models.CASCADE)
    student = models.ForeignKey(student_record, on_delete=models.CASCADE)
    hour_1_present = models.BooleanField(default=False, null=True)
    hour_2_present = models.BooleanField(default=False, null=True)
    hour_3_present = models.BooleanField(default=False, null=True)
    hour_4_present = models.BooleanField(default=False, null=True)
    hour_5_present = models.BooleanField(default=False, null=True)
    # Add fields to track user history
    def __str__(self):
        return f"{self.date} - {self.classroom} - {self.student}"



    
class Request(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    staff = models.ForeignKey(staff, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.staff.name} - {self.sender.username} - {self.status}"
    
class leave_letter(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    staff = models.ForeignKey(staff, on_delete=models.CASCADE)
    leave_type = [
        ('Sick Leave','Sick Leave'),('Parental Leave:','Parental Leave:'),('Educational Leave','Educational Leave'),
        ('Religious Observance Leave','Religious Observance Leave'),('Family Event Leave','Family Event Leave')
    ]
    type = models.CharField(max_length=100, choices=leave_type)
    start = models.DateField()
    end = models.DateField()
    message = models.TextField(blank = False)
    created = models.DateTimeField(auto_now_add=True)
   
class Iot (models.Model):
    data= models.IntegerField()