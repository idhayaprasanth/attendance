from django.shortcuts import render, redirect
from college.forms import ClassroomForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

@login_required
def create_class(request):
    user_belongs_to_staff = request.user.groups.filter(name='staff').exists()
    user_belongs_to_hod = request.user.groups.filter(name='hod').exists()

    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            new_class = form.save()
            return redirect('index')  # Assuming you have a class detail view
    else:
        form = ClassroomForm()

    return render(request, 'create_class.html', {
        'form': form,
        'user_belongs_to_staff': user_belongs_to_staff,
        'user_belongs_to_hod': user_belongs_to_hod
    })
