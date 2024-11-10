from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(models.Model):
    ROLE_CHOICES = [
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    ]
    
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name="Chức vụ")

    def __str__(self):
        return self.username

# Model Class
class Class(models.Model):
    class_name = models.CharField(max_length=100, verbose_name="Lớp học")
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, verbose_name="Giảng viên đứng lớp")
    
    def __str__(self):
        return self.class_name
    def student_count(self):
        return Student.objects.filter(class_name=self).count()

    def student_list(self):
        students_in_class = Student.objects.filter(class_name=self)
        return ', '.join([student.name for student in students_in_class])
    student_list.short_description = 'Danh sách sinh viên'

# Model Teacher
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, verbose_name="Tài khoản giảng viên")
    name = models.CharField(max_length=100, verbose_name="Tên")
    teacher_id = models.CharField(max_length=20, unique=True, null=True, verbose_name="Mã số giảng viên")

    def __str__(self):
        return self.name

# Model Student
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, verbose_name="Tài khoản sinh viên")
    name = models.CharField(max_length=100, verbose_name="Tên")
    student_id = models.CharField(max_length=20, unique=True, verbose_name="Mã số sinh viên")
    class_name = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, verbose_name="Danh sách lớp học phần")
    fingerprint_data = models.IntegerField(null=True, blank=True, verbose_name="Dữ liệu vân tay")
    
    def __str__(self):
        return self.name


# Model Attendance
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,verbose_name="Sinh viên")
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')], default='Present', verbose_name="Trạng thái điểm danh")

    def __str__(self):
        return f"{self.student.name} - {self.timestamp} - {self.status}"
