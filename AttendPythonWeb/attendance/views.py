from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Attendance, User

@csrf_exempt

def home(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pwd')
        std = User.objects.filter(username=username, password=password, role="Student").first()
        lec = User.objects.filter(username=username, password=password, role="Teacher").first()
        if std:
            return render(request, 'interface/student.html')
        if lec:
            return render(request, 'interface/lecturer.html')
    return render(request, 'login/login.html')
