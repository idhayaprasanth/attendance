# college/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import department,staff,classroom,student_record,attendance,leave_letter,Circular,Profile
from django.utils import timezone
from django.forms import formset_factory
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm



class CircularForm(forms.ModelForm):
    class Meta:
        model = Circular
        fields = ['user', 'department', 'image', 'message']

class LeaveLetterForm(forms.ModelForm):
    class Meta:
        model = leave_letter
        fields = ['staff','type', 'start', 'end', 'message']
class AttendanceSelectionForm(forms.ModelForm):
    classroom = forms.ModelChoiceField(queryset=classroom.objects.all(), empty_label=None, label='classroom')
    date = forms.DateField(initial=timezone.now, label='Date')
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = attendance
        fields = '__all__'
    
AttendanceFormSet = forms.modelformset_factory(
    attendance,
    form=AttendanceForm,
    extra=0,  # Do not include extra forms
)


class StudentForm(forms.ModelForm):
    class Meta:
        model = student_record
        fields = ['classroom','batch', 'reg', 'name', 'mobile', 'gender']
class ClassroomForm(forms.ModelForm):
    class Meta:
        model = classroom
        fields = '__all__'  # You can also specify the fields explicitly if you don't want to include all fields

    def __init__(self, *args, **kwargs):
        super(ClassroomForm, self).__init__(*args, **kwargs)
        # Set subjects fields as optional
        self.fields['subject5'].required = False
        self.fields['subject6'].required = False
        self.fields['subject7'].required = False
        self.fields['subject8'].required = False
        self.fields['subject9'].required = False
class StaffForm(forms.ModelForm):
    class Meta:
        model = staff
        fields = ['department', 'name', 'qualification', 'mobile']
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = department
        fields = ['name', 'user'] 
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
class CustomUserCreationForm(UserCreationForm):
    mobile_number = forms.CharField(max_length=15)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'mobile_number']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if Profile.objects.filter(mobile_number=mobile_number).exists():
            raise forms.ValidationError("This mobile number is already registered.")
        return mobile_number
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data