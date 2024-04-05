from django.shortcuts import render, redirect
from .forms import DepartmentForm,CircularForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from college.models import Request,student_record,department,attendance,classroom,staff,Iot,leave_letter,Circular
from django.contrib.auth.decorators import login_required
import datetime
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render

def iots(request):
    return render(request , 'iot.html')
def iot(request):
    try:
        iot_instance = Iot.objects.get(id=1)  # Assuming there's only one instance of Iot
        distance = iot_instance.data
    except Iot.DoesNotExist:
        distance = "Distance data not found"
        
    return JsonResponse({'distance': distance})

def sensor_data(request):
    if request.method == 'GET':
        distance = request.GET.get('distance', None)
        if distance is not None:
            # Process the received distance data as needed
            print("Received distance:", distance)
            # You can store this data in the database or do any other processing
            
            # Update the model instance with the received distance data
            iot_instance, created = Iot.objects.get_or_create(id=1)  # Assuming there's only one instance of Iot
            iot_instance.data = distance
            iot_instance.save()
            
            return HttpResponse(distance)
    return HttpResponse()

def index(request):
    if request.user.is_authenticated:
        if student_record.objects.filter(user=request.user).exists():
            students = student_record.objects.get(user=request.user)
            staffs = staff.objects.filter(department=students.classroom.department)
            today_date = datetime.date.today()
            attendance_records = attendance.objects.filter(student=students, date="2024-03-01")
            return render(request, 'student_landing.html', {'welcome_student': True, 'student': students, 'attendance_records': attendance_records,'staff':staffs})
        elif department.objects.filter(user=request.user).exists():
            department_obj = department.objects.get(user=request.user)
            pending_requests = Request.objects.filter(status='pending')
            pending_request_count = request.user.received_requests.filter(status='pending').count()
            return render(request, 'hod_landing.html', {'hod': True, 'department_obj': department_obj, 'pending_request_count': pending_request_count, 'requests': pending_requests})
        elif Request.objects.filter(sender=request.user, status='accepted').exists():
            staff_with_accepted_request = Request.objects.filter(sender=request.user, status='accepted')
            classrooms = None 
            leave = None
            student = None
            circular = None
             # Default value
            try:
                staff_obj = staff.objects.get(created_by=request.user)
                if isinstance(staff_obj.department, department):  # Ensure staff_obj.department is a department instance
                    classrooms = classroom.objects.filter(department=staff_obj.department)
                    student = student_record.objects.filter(classroom__in = classrooms)
                    
                leave = leave_letter.objects.filter(staff=staff_obj)
                circular = Circular.objects.filter(department = staff_obj.department)
              
                
                

            except staff.DoesNotExist:
                pass  # Handle the case when no staff object is found
            
            return render(request, 'staff_landing.html', {'staff_with_accepted_request': staff_with_accepted_request, 'class': classrooms,'leave':leave,'student':student,'circular':circular})
        else:
            return render(request, 'index.html')
    else:
        return redirect('login')

    
def create_department(request):
    users = User.objects.all()
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.user = request.user  # Associate the current user with the department
            department.save()
            # Handle redirection or response
    else:
        form = DepartmentForm()
    return render(request, 'create_department.html', {'form': form,'users':users})

def create_circular(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        message = request.POST.get('message')  # Corrected typo here
        user = request.user
        department_instance = department.objects.filter(user=user).first()  # Assuming there's only one department per user
        circular = Circular.objects.create(user=user, department=department_instance, image=image, message=message)
        response_data = {'message': 'Successfully created circular.'}
        return JsonResponse(response_data)