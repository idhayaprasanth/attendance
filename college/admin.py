from django.contrib import admin
from .models import  department, staff, classroom,  attendance,Request,student_record,Iot,leave_letter


class RequestAdmin(admin.ModelAdmin):
    list_display = ('staff', 'sender', 'receiver', 'status')
    list_filter = ('status',)
    search_fields = ('staff__name', 'sender__username', 'receiver__username')

admin.site.register(Request, RequestAdmin)
admin.site.register(leave_letter)
admin.site.register(Iot)

@admin.register(department)
class DepartmentAdmin(admin.ModelAdmin):
    pass

@admin.register(staff)
class StaffAdmin(admin.ModelAdmin):
    pass

@admin.register(classroom)
class ClassroomAdmin(admin.ModelAdmin):
    pass



@admin.register(student_record)
class Student_recordAdmin(admin.ModelAdmin):
    pass

@admin.register(attendance)
class AttendanceAdmin(admin.ModelAdmin):
    pass


 

