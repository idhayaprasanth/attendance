# views.py
from django.shortcuts import render, redirect
from college.forms import StudentForm
from college.models import student_record
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def add_student(request):
    # Check if the user already has a student record
    existing_student_record = student_record.objects.filter(user=request.user).first()
    if existing_student_record:
        messages.error(request, 'You have already created a student record.')
        return redirect('index')
    
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student_instance = form.save(commit=False)
            student_instance.user = request.user
            student_instance.save()
            return redirect('index')  # Redirect to a success page
    else:
        form = StudentForm()
    return render(request, 'create_student.html', {'form': form})

