from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Student, Attendance, Teacher, Class, User

@csrf_exempt
def home(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pwd')
        std = User.objects.filter(username=username, password=password, role="Student").first()
        lec = User.objects.filter(username=username, password=password, role="Teacher").first()
        if std:
            user = Student.objects.filter(user = std).first()
            context = {'user': user}
            return render(request, 'interface/student.html',context)
        if lec:
            user = Teacher.objects.filter(user = lec).first()
            classes = Class.objects.filter(teacher=user)
            context = {'user': user, 'classes': classes}
            return render(request, 'interface/lecturer.html',context)
    return render(request, 'login/login.html')
def getClass(request, id):
    classObj = Class.objects.get(id=id)
    students = Student.objects.filter(class_name = classObj)
    classes = Class.objects.filter(teacher=classObj.teacher)
    context = {
        'class': classObj,
        'students': students,
        'classes': classes
    }
    if request.method =='POST':
        for student in students:
            midScr = float(request.POST.get(f'midScr{student.id}'))
            fnlScr = float(request.POST.get(f'fnlScr{student.id}'))
            student.midScr = midScr
            student.fnlScr = fnlScr
            student.save()
    return render(request, 'interface/ClassManagement.html', context)
def getAttendanceList(request, id):
    classObj = Class.objects.get(id=id)
    students = Student.objects.filter(class_name = classObj)
    classes = Class.objects.filter(teacher=classObj.teacher)
    ListStudentAndHisStatuses = [] # Ở đây sẽ tạo một list chức các tuple gồm học sinh và status trong 15 ngày của học sinh đó 
    class_dates = classObj.get_class_dates()
    for student in students:
        statuses = student.getStatus()
        ListStudentAndHisStatuses.append({
            'student':student,
            'statuses':statuses,
        })
    context = {
        'class': classObj,
        'students_statuses': ListStudentAndHisStatuses,
        'class_dates': class_dates,
        'classes': classes
    }
    return render(request, 'interface/AttendForLecturer.html', context)
def getAttendForStudent(request, id):
    student = Student.objects.get(id=id)
    attendanceList = student.getStatus()
    context = {
        'student': student,
        'statusList': attendanceList
    }
    return render(request, 'interface/AttendanceForStudent.html', context)
def getMark(request, id):
    student = Student.objects.get(id=id)
    context = {
        'student': student
    }
    return render(request, 'interface/Mark.html', context)
def getAccountManagement(request,role,id):
    if role == 'student':
        user = Student.objects.get(id=id)
        classes = user.class_name
    elif role == 'lecturer':
        user = Teacher.objects.get(id=id)
        classes = Class.objects.filter(teacher=user)
    context = {
        'user': user,
        'classes': classes
    }
    if request.method=='POST':
        old_password = request.POST.get('oldPass')
        new_pass = request.POST.get('newPass')
        cfm_pass = request.POST.get('cfmPass')
        if old_password != user.user.password:
            messages.error(request, 'Wrong password')
        elif cfm_pass != new_pass:
            messages.error(request, 'New password does not match')
        else:
            messages.success(request, 'Changed password successfully')
            new_pass = request.POST.get('newPass')
            user.user.password = new_pass
            user.user.save()
    return render(request, 'interface/AccountManagement.html', context)