from django.shortcuts import render, redirect
from django.db.models import Q
from college.models import attendance,department,classroom,student_record,leave_letter,Request,staff,workingday
from django.shortcuts import render, get_object_or_404, redirect
from college.forms import AttendanceForm,LeaveLetterForm
from datetime import datetime
from django.forms import modelformset_factory
from django.utils.dateparse import parse_date
from django.contrib import messages
from datetime import date
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseNotAllowed
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required




def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            classroom = form.cleaned_data['classroom']
            student = form.cleaned_data['student']

            # Check if attendance already exists for the given parameters
            attendance_instances = attendance.objects.filter(
                Q(date=date) & Q(classroom=classroom) & Q(student=student)
            )

            if attendance_instances.exists():
                # Update existing attendance instance
                attendance_instance = attendance_instances.first()
                # Update only the fields that are changed in the form
                for field_name, field_value in form.cleaned_data.items():
                    # Check if the field is for hour present and if it's changed
                    if field_name.startswith('hour_') and field_value != getattr(attendance_instance, field_name):
                        setattr(attendance_instance, field_name, field_value)
                        # Track user history for each hour individually
                        setattr(attendance_instance, f"{field_name}_updated_by", request.user)
                attendance_instance.save()
            else:
                form.save()

            return redirect('index')
    else:
        form = AttendanceForm()
    return render(request, 'attendance.html', {'form': form})



def update(request, class_id, dates):
    try:
        classroom_obj = classroom.objects.get(id=class_id)
    except classroom.DoesNotExist:
        raise Http404("Classroom does not exist")

    students_in_classroom = student_record.objects.filter(classroom=classroom_obj)
    parsed_date = parse_date(dates)

    # Filter working days based on the classroom year and the current date
    today_date = date.today()
    working_queryset = workingday.objects.filter(year=classroom_obj.year, start__lte=today_date)
    
    working_instance = working_queryset.order_by('-start').first() if working_queryset.exists() else None

    # Create new attendance instances if they don't exist
    new_instances = []
    for student_in_classroom in students_in_classroom:
        if not attendance.objects.filter(student=student_in_classroom, date=parsed_date).exists():
            new_instance = attendance(
                classroom=classroom_obj,
                student=student_in_classroom,
                date=parsed_date,
                batch=working_instance.batch if working_instance else None,
                sem=working_instance.sem if working_instance else None
            )
            new_instances.append(new_instance)

    if new_instances:
        attendance.objects.bulk_create(new_instances)

    # Re-query the attendances after potential new instances have been created
    attendances = attendance.objects.filter(student__in=students_in_classroom, date=parsed_date)

    # Create the formset
    AttendanceFormSet = modelformset_factory(
        attendance,
        fields=('id', 'hour_1_present', 'hour_2_present', 'hour_3_present', 'hour_4_present', 'hour_5_present'),
        extra=0
    )

    if request.method == 'POST':
        formset = AttendanceFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                form.instance.batch = working_instance.batch if working_instance else form.instance.batch
                form.instance.sem = working_instance.sem if working_instance else form.instance.sem
                form.save()

            return redirect('index')
        else:
            print("Formset has validation errors:", formset.errors)
            print("Non-form errors:", formset.non_form_errors())
    else:
        formset = AttendanceFormSet(queryset=attendances)

    return render(request, 'update_attendance.html', {'formset': formset})

def attendance_record(request):
    if request.method == 'POST':
        classroom_id = request.POST.get('classroom_id')
        dates = request.POST.get('dates')
        
        # Retrieve attendance records based on the given parameters
        attendance_records = attendance.objects.filter(classroom=classroom_id, date=dates)
        
        if attendance_records.exists():
            # Attendance records found, render the template with the records
            return render(request, 'attendance_record.html', {'records': attendance_records,'all':True})
        else:
            # No attendance records found, display an appropriate message
            return render(request, 'attendance_record.html')
    else:
        # Handle other HTTP methods if needed
        return HttpResponse(status=405)
      # Method Not AllowedMethod Not Allowed
def search_student(request):
    if request.method == 'POST':
        classroom_id = request.POST.get('classroom_id')
        reg = request.POST.get('reg')
        if reg == "all":
            student_records = student_record.objects.filter(classroom=classroom_id).order_by('name')       
            return render(request,'student_record.html',{'student':student_records})
        else:
            student_records = student_record.objects.filter(classroom=classroom_id, reg=reg).order_by('name')
            if student_records.exists():
                return render(request,'student_record.html',{'student':student_records})
            else:
                return render(request, 'student_record.html')
    else:
        # Handle other HTTP methods if needed
        return HttpResponse(status=405)  
def calculate_attendance(sem_records, sem_number):
    if sem_records.exists():
        first_record = sem_records.first()
        working_queryset = workingday.objects.filter(batch=first_record.batch, sem=sem_number)
        working_day_record = working_queryset.first()

        if working_day_record:
            total_working_days = working_day_record.workingday
            total_present_days = 0
            total_leave_days = 0

            for record in sem_records:
                if record.present == 'Full Day':
                    total_present_days += 1
                elif record.present == 'Half Day':
                    total_present_days += 0.5
                elif record.present == 'Leave':
                    total_leave_days += 1

            total_days = total_present_days + total_leave_days
            percentage_present = (total_present_days / total_working_days) * 100 if total_working_days > 0 else 0

            return {
                'sem_records': sem_records,
                'total_working_days': total_working_days,
                'total_present_days': total_present_days,
                'total_leave_days': total_leave_days,
                'total_days': total_days,
                'percentage_present': percentage_present
            }
    return None

def all_attendance(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = student_record.objects.get(reg=student_id)
        if student_id:
            try:
                semesters = [1, 2, 3, 4, 5, 6]
                attendance_data = {}

                for sem in semesters:
                    sem_records = attendance.objects.filter(student__reg=student_id, sem=sem).order_by('date')
                    attendance_data[f'sem{sem}'] = calculate_attendance(sem_records, sem)

                # Sort the attendance_data dictionary by key in descending order
                sorted_attendance_data = dict(sorted(attendance_data.items(), key=lambda x: x[0], reverse=True))

                if any(sorted_attendance_data.values()):  # Check if there's any non-None attendance data
                    context = {key: value for key, value in sorted_attendance_data.items() if value is not None}
                    return render(request, 'all_attendance.html', {'context': context,'student':student})
                else:
                    return render(request, 'all_attendance.html', {'error': 'No attendance records found'})

            except ValueError:
                return render(request, 'all_attendance.html', {'error': 'Invalid student ID'})
        else:
            return render(request, 'all_attendance.html', {'error': 'No student ID provided'})
    else:
        return render(request, 'all_attendance.html')




def leave_letters(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff')
        leave_type = request.POST.get('type')
        start_date = request.POST.get('start')
        end_date = request.POST.get('end')
        message = request.POST.get('message')
        user = request.user
        leave_obj = leave_letter.objects.create(user=user,staff_id=staff_id, type=leave_type,
                                               start=start_date, end=end_date, message=message)

        messages.success(request, 'Leave letter submitted successfully.')
        return redirect('index')
  
@login_required
@require_POST
def mark_leave_letter_as_seen(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    staff_obj = staff.objects.get(created_by=request.user)
    # Ensure leave_letter object exists and belongs to the current user
    leave_letter_obj = leave_letter.objects.filter(staff=staff_obj, seen=False).first()

    if leave_letter_obj:
        # Update 'seen' field and save the object
        leave_letter_obj.seen = True
        leave_letter_obj.save()

    return redirect('index')
def test(request):
    if request.method == 'GET':
        date_obj = request.GET.get('date')
        students = student_record.objects.get(user=request.user)
        attendance_records = attendance.objects.filter(student=students, date=date_obj)
        
        context = {
            'records': attendance_records
        }
        return render(request, 'attendance_record.html', context)
    else:
        # Handle other HTTP methods if needed
        return HttpResponse(status=405)

def percentage(request):
    if request.method == 'POST':
        classroom_id = request.POST.get('classroom_id')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        student_records = student_record.objects.filter(classroom=classroom_id)
        
        students_attendance = {}  # Dictionary to store each student's attendance details
        
        for student in student_records:
            attendance_records = attendance.objects.filter(
                student=student,
                date__range=[start_date, end_date]
            )

            total_working_days = 4  # Assuming total working days
            total_present_days = 0
            total_leave_days = 0
            
            for record in attendance_records:
                if record.present == 'Full Day':
                    total_present_days += 1
                elif record.present == 'Half Day':
                    total_present_days += 0.5
                elif record.present == 'Leave':
                    total_leave_days += 1
            total_days = total_present_days + total_leave_days
            percentage_present = (total_present_days / total_working_days) * 100

            # Store student's attendance details in the dictionary
            students_attendance[student] = {
                'percentage_present': percentage_present,
                'total_leave_days': total_leave_days,
                'total_days': total_days,
                'total_working_days': total_working_days
            }

        # Pass the students_attendance dictionary to the template context
        context = {
            'students_attendance': students_attendance
        }

        # You can return the context along with your HTML template
        return render(request, 'student_record.html', context)
    else:
        return HttpResponse("ERROR")
 
     
def all_student_attendance(request):
    if request.method == 'POST':
        classroom_id = request.POST.get('classroom_id')
        sem_number = request.POST.get('semester')
        classrooms = classroom.objects.get(id = classroom_id)

        # Adjusted the filter to use the classroom object instead of classroom_id
        sem_records = attendance.objects.filter(
            classroom=classroom_id,  # Use the classroom object
            sem=sem_number
        ).order_by('date','student__name')

        return render(request, 'all_student_attendance.html',{'attendance_data':sem_records,'classroom':classrooms} )
    else:
        return render(request, 'all_student_attendance.html', {'error': 'No attendance records found'})
    return render(request, 'all_student_attendance.html')
         
def all_student_percentage(request):
    if request.method == 'POST':
        classroom_id = request.POST.get('classroom_id')
        semester = request.POST.get('semester')
        classrooms = classroom.objects.get(id=classroom_id)
        
        # Filter the attendance records based on the classroom and semester
        students = student_record.objects.filter(classroom=classroom_id).order_by('name')
        if not students.exists():
            # Handle the case where no students are found
            return render(request, 'attendance/attendance_form.html', {'class': classroom.objects.all(), 'error': 'No students found for this classroom'})

        # Get the batch from the first student (assuming all students in a classroom are from the same batch)
        batch = students.first().batch
        
        working_queryset = workingday.objects.filter(batch=batch, sem=semester)
        
        if working_queryset.exists():
            working_instance = working_queryset.order_by('-start').first()
            total_working_days = working_instance.workingday

            student_attendance_data = []

            for student in students:
                present_records = attendance.objects.filter(
                    student=student,
                    date__range=[working_instance.start, working_instance.end]
                )

                total_present_days = present_records.filter(present='Full Day').count()
                total_present_days += present_records.filter(present='Half Day').count() * 0.5
                total_leave_days = present_records.filter(present='Leave').count()
                total_days = total_present_days + total_leave_days
                percentage_present = (total_present_days / total_working_days) * 100 if total_working_days > 0 else 0

                student_attendance_data.append({
                    'student': student,
                    'total_present_days': total_present_days,
                    'total_leave_days': total_leave_days,
                    'total_working_days': total_working_days,
                    'percentage_present': percentage_present
                })

            context = {
                'student_attendance_data': student_attendance_data,
                'classroom': classrooms,
                'semester': semester
            }
            return render(request, 'attendance_percentage.html', context)
    

    return render(request, 'attendance_percentage.html', {'class': classroom.objects.all()})