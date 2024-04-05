# views.py
from django.shortcuts import render, redirect
from college.forms import StudentForm

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to a success page
    else:
        form = StudentForm()
    return render(request, 'create_student.html', {'form': form})
