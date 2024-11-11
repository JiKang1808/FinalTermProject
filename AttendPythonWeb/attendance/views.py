from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
    context = {
        'class': classObj,
        'students': students
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
    context = {
        'class': classObj,
        'students': students
    }
    return render(request, 'interface/AttendForLecturer.html', context)