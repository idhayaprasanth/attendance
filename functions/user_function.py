from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from college.forms import CustomUserCreationForm
from college.models import Profile
import random
from django.contrib.auth.models import User
from django.conf import settings
from django.db import IntegrityError
from django.core.mail import send_mail
from django.template.loader import render_to_string



#login a existed user


# create a new user
def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save user yet
            mobile_number = form.cleaned_data.get('mobile_number')
            email = form.cleaned_data.get('email')

            # Save the user
            user.save()

            # Try to get the existing profile associated with the user
            try:
                profile = Profile.objects.get(user=user)
                # Update the existing profile with the new data
                profile.mobile_number = mobile_number
                profile.email = email
                profile.save()
            except Profile.DoesNotExist:
                # If no profile exists, create a new one
                profile = Profile.objects.create(user=user, mobile_number=mobile_number, email=email)
                
            return redirect('index')  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
# logout the new user

def user_logout(request):
    logout(request)
    return redirect('login')


def user_login(request):
    error_message = None

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')

            else:
                error_message = "Invalid username or password. Please try again."

        else:
            error_message = "Invalid username or password. Please try again."

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form, 'error_message': error_message})
def send_otp_email(email, otp):
    subject = 'OTP for Password Reset'
    message = f'Your OTP is: {otp}'
    sender_email = 'idhayaprasanth56@gmail.com'  # Change this to your email address

    send_mail(subject, message, sender_email, [email])

def password_reset_with_otp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)

            # Generate OTP
            otp = generate_otp()

            # Send OTP to the email associated with the profile
            send_otp_email(profile.email, otp)

            # Store username and OTP in session
            request.session['reset_username'] = username
            request.session['otp'] = otp

            # Redirect to OTP verification page
            return redirect('otp_verification')

        except User.DoesNotExist:
            error_message = "User does not exist."
            return render(request, 'forget_pass.html', {'error_message': error_message})
    return render(request, 'forget_pass.html')
def generate_otp():
    # Generate a random 6-digit OTP
    return ''.join(random.choices('0123456789', k=6))

def otp_verification(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        username = request.session.get('reset_username')

        if entered_otp == stored_otp:
            return redirect('reset_password', username=username)

        else:
            error_message = "Invalid OTP. Please try again."
            return render(request, 'otp_verification.html', {'error_message': error_message})

    return render(request, 'otp_verification.html')

def reset_password(request, username):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect('login')

        else:
            error_message = "Passwords do not match."
            return render(request, 'reset_password.html', {'error_message': error_message})

    return render(request, 'reset_password.html')