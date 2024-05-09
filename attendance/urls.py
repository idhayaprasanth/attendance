"""
URL configuration for attendance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from functions  import user_function,staff_request,classroom,student,attendance
from college import views


urlpatterns = [
    path('', views.index, name='index'),
    
    path('iot/', views.iot, name='iot'),
    path('sensor_data/', views.sensor_data, name='sensor_data'),
    path('admin/', admin.site.urls),
    path('delete_staff/<int:staff_id>/',staff_request.delete_staff,name="delete_staff"),
    path('percentage/',attendance.percentage,name='percentage'),
    path('create_circular/',views.create_circular,name="create_circular"),
    path('test/',attendance.test,name='test'),
    path('leave/', attendance.leave_letters, name='leave'),
    path('update/<str:class_id>/<str:dates>/',attendance.update,name='update'),
    path('attendance_record',attendance.attendance_record,name='attendance_record'),
    path('search_student',attendance.search_student,name='search_student'),
    path('attendance/',attendance.mark_attendance,name='mark_attendance'),
    path('student/', student.add_student, name='add_student'),
    path('classroom/',classroom.create_class,name='create_class'),
    path('staff/', staff_request.register_staff, name='register_staff'),
    path('request/<int:request_id>/accept/', staff_request.accept_request, name='accept_request'),
    path('request/<int:request_id>/decline/', staff_request.decline_request, name='decline_request'),
    path('index',views.index,name='index'),
    path("cdepartment",views.create_department,name='create_department'),
    path('register/', user_function.user_register, name='register'),
    path('login/', user_function.user_login, name='login'),
    path('logout/', user_function.user_logout, name='logout'),
  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
