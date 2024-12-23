from django.contrib import admin
from .models import Schedule1
from .models import Teacher,AssignTeacher

@admin.register(Schedule1)
class Schedule1Admin(admin.ModelAdmin):
    list_display = ('schedule_id', 'date_time', 'no_of_exams', 'no_of_rooms_req')
    # Add any other configurations for Schedule1 admin if needed

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'teacher_id')
    # Add any other configurations for Teacher admin if needed

@admin.register(AssignTeacher)
class AssignTeacherAdmin(admin.ModelAdmin):
    list_display = ( 'date_time', 'block', 'room_number', 'no_of_students', 'teacher1', 'teacher2')
    # Add any other configurations for AssignTeacher admin if needed