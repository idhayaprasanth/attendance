from django.shortcuts import render, redirect
from django.db.models import Q
from college.models import attendance,department,classroom,student_record,leave_letter,Request,staff
from django.shortcuts import render, get_object_or_404, redirect
from college.forms import AttendanceForm,LeaveLetterForm
from datetime import datetime
from django.forms import modelformset_factory
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed





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



# views.py

def update(request, class_id, dates):
    try:
        classroom_obj = classroom.objects.get(id=class_id)
    except classroom.DoesNotExist:
        # Handle the case where the classroom does not exist
        # You may redirect the user to an error page or return an error message
        # Here, we're just raising an Http404 for simplicity
        raise Http404("Classroom does not exist")

    students_in_classroom = student_record.objects.filter(classroom=classroom_obj)
    attendances = attendance.objects.filter(student__in=students_in_classroom, date=parse_date("2024-03-01"))

    # Create new attendance instances if they don't exist
    parsed_date = parse_date(dates)
    new_instances = []

    for student_in_classroom in students_in_classroom:
        try:
            attendance.objects.get(student=student_in_classroom, date=parsed_date)
        except attendance.DoesNotExist:
            new_instance = attendance(
                classroom=classroom_obj,
                student=student_in_classroom,
                date=parsed_date
            )
            new_instances.append(new_instance)

    if new_instances:
        attendance.objects.bulk_create(new_instances)

    # Re-query the attendances after potential new instances have been created
    attendances = attendance.objects.filter(student__in=students_in_classroom, date=dates)

    # Create the formset
    AttendanceFormSet = modelformset_factory(
        attendance,
        fields=('id', 'hour_1_present', 'hour_2_present', 'hour_3_present', 'hour_4_present', 'hour_5_present'),
        extra=0
    )
    
    if request.method == 'POST':
        formset = AttendanceFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            print("Changes saved successfully.")
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
            return render(request, 'attendance_record.html', {'records': attendance_records})
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
            student_records = student_record.objects.filter(classroom=classroom_id)        
            return render(request,'student_record.html',{'student':student_records})
        else:
            student_records = student_record.objects.filter(classroom=classroom_id, reg=reg)
            if student_records.exists():
                return render(request,'student_record.html',{'student':student_records})
            else:
                return render(request, 'student_record.html')
    else:
        # Handle other HTTP methods if needed
        return HttpResponse(status=405)  

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
    
        


def test(request, student_id,date):
    students = get_object_or_404(student_record, id=student_id)
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()  # Convert string date to datetime object
    attendance_records = attendance.objects.filter(student=students, date=date_obj)

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            # Update attendance records
            for record in attendance_records:
                record.hour_1_present = form.cleaned_data['hour_1_present']
                record.hour_2_present = form.cleaned_data['hour_2_present']
                record.hour_3_present = form.cleaned_data['hour_3_present']
                record.hour_4_present = form.cleaned_data['hour_4_present']
                record.hour_5_present = form.cleaned_data['hour_5_present']
                record.save()
            return redirect('index')  # Redirect to a success page
    else:
        form = AttendanceForm()

    context = {
        'student': students,
        'attendance_records': attendance_records,
        'form': form,
    }
    return render(request, 'test.html', context)

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
 
     
            
         
