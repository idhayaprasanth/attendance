from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from college.forms import StaffForm
from college.models import Request
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group



# Register staff and handle form submission, validation, and notification.
@login_required
def register_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            staff_instance = form.save(commit=False)
            staff_instance.user = request.user
            staff_instance.save()
            send_request(staff_instance, request.user)
            messages.success(request, 'Staff registration successful!')
            return redirect('index')  
        else:
            print(form.errors)
            messages.error(request, 'Staff registration failed. Please correct the errors.')
    else:
        form = StaffForm()
    return render(request, 'register_staff.html', {'form': form})


# Send a registration request to the department superuser based on staff details.
def send_request(staff_instance, sender):
    department_name = staff_instance.department.name
    department_users = User.objects.filter(department__name=department_name)
    if department_users.exists():
        receiver = department_users.first()
        Request.objects.create(sender=sender, receiver=receiver, staff=staff_instance)

# Accept a staff registration request and notify the sender.
def accept_request(request, request_id):
    request_obj = Request.objects.get(id=request_id)
    request_obj.status = 'accepted'
    request_obj.save()   
    # Add the user to the staff group
    staff_group = Group.objects.get(name='staff')  # Assuming 'Staff' is the name of the staff group
    staff_group.user_set.add(request_obj.sender)   # Add the sender (staff user) to the staff group
    messages.success(request, f"Your request from {request_obj.sender.username} has been accepted!")
    return redirect('index')

# Decline a staff registration request and inform the sender.
def decline_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    req.status = 'declined'
    req.save()
    messages.info(request, 'Request declined!')
    return redirect('index')
