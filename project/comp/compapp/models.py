from sched import scheduler
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.utils.timezone import localtime

class UserProfile(models.Model):  # Renamed from 'user' to 'UserProfile'
    user = models.OneToOneField(User, on_delete=models.CASCADE)

ROOM_CHOICES = {
    'sblock': [
        ('S001', 'S001'),
        ('S002', 'S002'),
        ('S003', 'S003'),
        ('S004', 'S004'),
    ],
    'nblock': [
        ('N001', 'N001'),
        ('N002', 'N002'),
        ('N003', 'N003'),
        ('N004', 'N004'),
    ],
    'ablock': [
        ('A001', 'A001'),
        ('A002', 'A002'),
        ('A003', 'A003'),
        ('A005', 'A005'),
    ],
}


class Schedule1(models.Model):
    SCHEDULE_CHOICES = [
        ('Midsem test', 'Midsem test'),
        ('Endsem test', 'Endsem test'),
        ('Makeup test', 'Makeup test'),
        ('Retest', 'Retest'),
    ]

    schedule_id = models.CharField(max_length=20, choices=SCHEDULE_CHOICES)
    date_time = models.DateTimeField(default=datetime.now() + timedelta(days=1))  # ForeignKey to represent date and time
    no_of_exams = models.IntegerField()
    no_of_rooms_req = models.IntegerField()

class Teacher(models.Model):
    name = models.CharField(max_length=25)
    department = models.CharField(max_length=25)
    teacher_id = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return self.name
    


BLOCK_CHOICES = (
    ('NEW_BLOCK', 'New Block'),
    ('ARRUPE_BLOCK', 'Arrupe Block'),
    ('SCIENCE_BLOCK', 'Science Block'),
)

ROOM_CHOICES = {
    'NEW_BLOCK': [
        ('N001', 'N001'),
        ('N002', 'N002'),
        ('N003', 'N003'),
        # Add more choices as needed
    ],
    'ARRUPE_BLOCK': [
        ('A001', 'A001'),
        ('A002', 'A002'),
        ('A003', 'A003'),
        # Add more choices as needed
    ],
    'SCIENCE_BLOCK': [
        ('S001', 'S001'),
        ('S002', 'S002'),
        ('S003', 'S003'),
        # Add more choices as needed
    ],
}


class AssignTeacher(models.Model):
    date_time = models.ForeignKey(Schedule1, on_delete=models.CASCADE,default=datetime.now() + timedelta(days=1))
    block = models.CharField(max_length=25)
    room_number = models.CharField(max_length=15)
    no_of_students = models.IntegerField()
    teacher1 = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher1')
    teacher2 = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher2', blank=True, null=True)
