from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
from .models import Schedule1
from django.shortcuts import render, redirect
from .models import Teacher,AssignTeacher
from .models import AssignTeacher
from django.shortcuts import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
import logging
import json
from django.contrib.auth import logout
from django.shortcuts import redirect
import csv
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponseBadRequest
from django.conf import settings
from django.db.models import Q

@csrf_exempt

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            if user.username == 'coe':  # Check if the username is COE
                return redirect('index1')  # Redirect COE to index1
            else:
                return redirect('User_report')  # Redirect other users to user_report
        else:
            return render(request, 'log.html', {'error': 'Invalid login credentials'})

    return render(request, 'log.html')

def logout_view(request):
    logout(request)
    return redirect('login_view')


def index(request):
    return render(request, 'index1.html')


def add_schedule(request):
    if request.method == 'POST':
        schedule_id=request.POST.get('schedule_id')
        date_time=request.POST.get('date_time')
        no_of_exams=request.POST.get('no_of_exams')
        no_of_rooms_req=request.POST.get('no_of_rooms_req')
        sec=Schedule1(schedule_id=schedule_id,date_time=date_time,no_of_exams=no_of_exams, no_of_rooms_req= no_of_rooms_req)
        sec.save()

        messages.success(request, 'Schedule added successfully.')  # success message

        # Redirect to the same page
        return HttpResponseRedirect(request.path)
    return render(request, 'Schedule.html')


def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_list.html', {'teachers': teachers})

def add_teacher(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        department = request.POST.get('department')
        teacher_id = request.POST.get('teacher_id')

        if not (name and department and teacher_id):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        # Assuming you have a Teacher model defined with fields name, department, teacher_id
        teacher = Teacher.objects.create(name=name, department=department, teacher_id=teacher_id)
        teacher.save()
        return redirect('add_teacher')  # Redirect to the same page after form submission
    else:
        teachers = Teacher.objects.all()  # Retrieve all teachers
        return render(request, 'teacher.html', {'teachers': teachers})


def delete_teacher(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        teacher_id = data.get('teacher_id')
        try:
            teacher = Teacher.objects.get(teacher_id=teacher_id)
            teacher.delete()
            return HttpResponse(status=204)  # Success, no content response
        except Teacher.DoesNotExist:
            return HttpResponse(status=404)  # Teacher not found
    else:
        return HttpResponse(status=405)  # Method not allowed
    


logger = logging.getLogger(__name__)

def edit_teacher(request, teacher_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        logger.info(f"Received data for editing teacher {teacher_id}: {data}")
        name = data.get('name')
        department = data.get('department')
        try:
            teacher = Teacher.objects.get(teacher_id=teacher_id)
            teacher.name = name
            teacher.department = department
            teacher.save()
            logger.info(f"Teacher {teacher_id} updated successfully.")
            return JsonResponse({'success': True})  # Return a success response
        except Teacher.DoesNotExist:
            logger.error(f"Teacher with ID {teacher_id} not found.")
            return JsonResponse({'success': False, 'error': 'Teacher not found'}, status=404)
    else:
        logger.error("Invalid request method.")
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


def assign_teacher(request):
    if request.method == 'POST':
        # Extract form data
        datetime_str = request.POST.get('datetime')
        if not datetime_str:
            return HttpResponseBadRequest('Missing datetime value')

        # Add a T separator between the date and time components
        datetime_list = datetime_str.split(' ')
        if len(datetime_list) != 2:
            return HttpResponseBadRequest('Invalid datetime format')

        date_str = datetime_list[0]
        time_str = datetime_list[1]
        datetime_str = f'{date_str}T{time_str}'

        date_time = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')  # Convert string to datetime object
        formatted_date_time = date_time.strftime('%Y-%m-%d %H:%M')  # Convert to desired format

        no_of_students = int(request.POST.get('no_of_students'))  # Convert to integer
        block = request.POST.get('block')
        room_number = request.POST.get('room_number')
        teacher_1_id = request.POST.get('teacher_1')

        # Retrieve schedule and teacher objects from the database
        try:
            scheduled = Schedule1.objects.get(date_time=formatted_date_time)  # Filter by date_time field
        except Schedule1.DoesNotExist:
            return HttpResponseBadRequest('Invalid schedule')

        try:
            teacher1 = Teacher.objects.get(teacher_id=teacher_1_id)
        except Teacher.DoesNotExist:
            return HttpResponseBadRequest('Invalid teacher 1')

        # Check if the teacher is already assigned to a different room at the same time
        teacher_assigned = AssignTeacher.objects.filter(
            Q(date_time=scheduled) & (Q(teacher1=teacher1) | Q(teacher2=teacher1))
        ).exists()
        
        if teacher_assigned:
            messages.error(request, 'This teacher is already assigned for another room at the same time.')
            return redirect('assign_teacher')  # Redirect back to the assignment page
            
        teacher2 = None
        if no_of_students >= 30:  # Only retrieve teacher_2 if number of students is 30 or more
            teacher_2_id = request.POST.get('teacher_2')
            try:
                teacher2 = Teacher.objects.get(teacher_id=teacher_2_id)
            except Teacher.DoesNotExist:
                return HttpResponseBadRequest('Invalid teacher 2')

        # Create a new AssignTeacher object and save it to the database
        assignment = AssignTeacher(
            date_time=scheduled,
            no_of_students=no_of_students,
            block=block,
            room_number=room_number,
            teacher1=teacher1,
            teacher2=teacher2
              # Assign formatted date_time
        )
        assignment.save()
        messages.success(request, 'Teacher assigned successfully.')
        return redirect('assign_teacher')  # Redirect to the assign_teacher page after saving

    # Retrieve schedules and teachers for rendering the form
    schedules = Schedule1.objects.all()
    teachers = Teacher.objects.all()

    return render(request, 'assign_teacher.html', {'schedules': schedules, 'teachers': teachers})


def report(request):
    department = request.GET.get('department')  # Get the entered department from the request

    # Filter teachers by department if department is specified
    if department:
        teachers = Teacher.objects.filter(department__icontains=department)
        assignteachers = AssignTeacher.objects.filter(teacher1__in=teachers) | AssignTeacher.objects.filter(teacher2__in=teachers)
    else:
        assignteachers = AssignTeacher.objects.all()  # Get all assignments if department is not specified

    return render(request, 'report.html', {'assignteachers': assignteachers})



def report_view(request):
    department = request.GET.get('department')

    if department:
        assignteachers = AssignTeacher.objects.filter(teacher1__department__icontains=department) | AssignTeacher.objects.filter(teacher2__department__icontains=department)
    else:
        assignteachers = AssignTeacher.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date and time', 'block', 'room', 'number of students', 'Teacher1', 'Teacher2'])

    for assign_teacher in assignteachers:
        writer.writerow([
            assign_teacher.date_time,
            assign_teacher.block,
            assign_teacher.room_number,
            assign_teacher.no_of_students,
            assign_teacher.teacher1,
            assign_teacher.teacher2
        ])

    return response

def User_report(request):
    department = request.GET.get('department')  # Get the entered department from the request

    # Filter teachers by department if department is specified
    if department:
        teachers = Teacher.objects.filter(department__icontains=department)
        assignteachers = AssignTeacher.objects.filter(teacher1__in=teachers) | AssignTeacher.objects.filter(teacher2__in=teachers)
    else:
        assignteachers = AssignTeacher.objects.all()  # Get all assignments if department is not specified

    return render(request, 'User_report.html', {'assignteachers': assignteachers})


def User_report_view(request):
   department = request.GET.get('department')

   if department:
        assignteachers = AssignTeacher.objects.filter(teacher1__department__icontains=department) | AssignTeacher.objects.filter(teacher2__department__icontains=department)
   else:
        assignteachers = AssignTeacher.objects.all()

   response = HttpResponse(content_type='text/csv')
   response['Content-Disposition'] = 'attachment; filename="report.csv"'

   writer = csv.writer(response)
   writer.writerow(['Date and time', 'block', 'room', 'number of students', 'Teacher1', 'Teacher2'])

   for assign_teacher in assignteachers:
        writer.writerow([
            assign_teacher.date_time,
            assign_teacher.block,
            assign_teacher.room_number,
            assign_teacher.no_of_students,
            assign_teacher.teacher1,
            assign_teacher.teacher2
        ])

   return response