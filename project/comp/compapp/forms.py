from django import forms
from .models import Schedule1,ROOM_CHOICES
from .models import Teacher,AssignTeacher


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule1
        fields = ['schedule_id', 'date_time', 'no_of_exams', 'no_of_rooms_req']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'name', 'department']

