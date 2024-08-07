from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()



class department(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class staff(models.Model):
    department = models.ForeignKey(department,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    mobile = models.IntegerField(unique=True)
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
        return f"  {self.year} -{self.section}-{self.department}"
    

class batch(models.Model):
    start = models.DateField()
    end = models.DateField()

    @property
    def years(self):
        return (self.start.year, self.end.year)
    
    def __str__(self):
        return f"  {self.start.year} -{self.end.year}"
    

class student_record(models.Model):  
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    batch = models.ForeignKey(batch,on_delete=models.CASCADE,null=True)
    classroom = models.ForeignKey(classroom,on_delete=models.CASCADE)
    reg = models.SlugField(max_length=20,unique=True)
    name=models.CharField(max_length=100)
    mobile = models.IntegerField(unique=True)
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
    PRESENT_CHOICES = [
        ('Full Day', 'Full Day'),
        ('Half Day', 'Half Day'),
        ('Leave', 'Leave'),
    ]
    present = models.CharField(max_length=8,default='Leave', choices=PRESENT_CHOICES, null=True)
    batch = models.ForeignKey(batch, on_delete=models.CASCADE, default=1)  # Set a default value here
    sem = models.CharField(max_length=1, default=1)

    def calculate_present_status(self):
        if self.hour_1_present and self.hour_2_present and self.hour_3_present and self.hour_4_present and self.hour_5_present:
            self.present = "Full Day"
        elif (self.hour_1_present and self.hour_2_present) or (self.hour_3_present and self.hour_4_present and self.hour_5_present):
            self.present = "Half Day"
        else:
            self.present = "Leave"

    def save(self, *args, **kwargs):
        self.calculate_present_status()
        super(attendance, self).save(*args, **kwargs)

    
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
    seen = models.BooleanField(default=False)

class Circular(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(department, on_delete=models.CASCADE)  # Correcting the department ForeignKey
    image = models.ImageField(blank=True)
    message = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)



class workingday(models.Model):
    batch = models.ForeignKey(batch,on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
       
    ]
    sem = models.CharField(max_length=1, choices=STATUS_CHOICES)
    year_choice = [
        ('1st', '1st'),('2nd','2nd'),('3rd','3rd'),
    ]
    year=models.CharField(max_length=3,choices=year_choice,default=1)
    workingday = models.IntegerField()
    start = models.DateField()
    end = models.DateField(null=True)

    

class Iot (models.Model):
    data= models.IntegerField()