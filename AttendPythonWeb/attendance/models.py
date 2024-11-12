from django.db import models

import datetime
from datetime import timedelta, datetime
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
    start_date = models.DateField(default=datetime.now,verbose_name="Ngày bắt đầu")
    start_time = models.TimeField(null=True, verbose_name="Giờ học")
    # Một giảng viên có thể dạy nhiều lớp 
    
    def __str__(self):
        return self.class_name
    def student_count(self):
        return Student.objects.filter(class_name=self).count()

    def student_list(self):
        students_in_class = Student.objects.filter(class_name=self)
        return ', '.join([student.name for student in students_in_class])
    student_list.short_description = 'Danh sách sinh viên'
    def get_class_dates(self):
        class_dates = [self.start_date + timedelta(days=7*i) for i in range(15)]
        return class_dates
    def get_full_datetime(self, date):
        return datetime.combine(date, self.start_time)

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
    # Một lớp có thể chứa nhiều học sinh
    midScr = models.FloatField(default=0,verbose_name="Điểm giữa kì")
    fnlScr = models.FloatField(default=0,verbose_name="Điểm cuối kỳ")
    fingerprint_data = models.IntegerField(null=True, blank=True, verbose_name="Dữ liệu vân tay")
    def Total(self):
        if self.midScr is not None and self.fnlScr is not None:
            return (self.midScr + self.fnlScr) / 2
        return 0
    def Arrange(self):
        if self.Total() > 8:
            return "Giỏi"
        elif self.Total() > 6.5:
            return "Khá"
        elif self.Total() > 5:
            return "Trung bình"
        else:
            return "Yếu"
    def __str__(self):
        return self.name
    def getAttendance(self):
        attendances = Attendance.objects.filter(student=self)
        return attendances
    # def get_status(self, date, begin_time):
    #     attendance = Attendance.objects.filter(timestamp__date=date, student=self).first()
    #     if attendance:
    #         if attendance.timestamp.time() > begin_time:
    #             return 'Late'
    #         elif attendance.timestamp.time() <= begin_time:
    #             return 'Present'
    #     return 'Absent'
    def getStatus(self):
        sttLst = []
        for date in self.class_name.get_class_dates():
            attendance = Attendance.objects.filter(timestamp__date=date, student=self).first()
            if attendance:
                if attendance.timestamp.time() > self.class_name.start_time:
                    sttLst.append('Late')
                elif attendance.timestamp.time() <= self.class_name.start_time:
                    sttLst.append('Present')
            else:
                sttLst.append('Absent')
        return sttLst
    def getClassDates(self):
        classDates = self.class_name.get_class_dates()
        return classDates

# Model Attendance
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,verbose_name="Sinh viên")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian điểm danh" )
    def __str__(self):
        return f"{self.student.name} - {self.timestamp} "


