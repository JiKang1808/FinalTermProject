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
    ListStudentAndHisStatuses = [] # Ở đây sẽ tạo một list chức các tuple gồm học sinh và status trong 15 ngày của học sinh đó 
    class_dates = classObj.get_class_dates()
    for student in students:
        statuses = student.getStatus()
        ListStudentAndHisStatuses.append({
            'student':student,
            'statuses':statuses
        })
    context = {
        'class': classObj,
        'students_statuses': ListStudentAndHisStatuses,
        'class_dates': class_dates
    }
    return render(request, 'interface/AttendForLecturer.html', context)
