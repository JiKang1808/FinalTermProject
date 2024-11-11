from django.contrib import admin
from django import forms
from .models import User, Student, Teacher, Class, Attendance
from django.utils.timezone import localtime
from django.utils.html import format_html
# Tùy chỉnh Admin cho User
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'role']
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'student_id', 'class_name']
    list_filter = ['class_name']

    # Ẩn nút "Add"
    def has_add_permission(self, request):
        return False


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher_id']

    # Ẩn nút "Add"
    def has_add_permission(self, request):
        return False
class StudentInline(admin.TabularInline):
    model = Student
    fields = ['name', 'student_id', 'fingerprint_data']
    readonly_fields = ['name', 'student_id', 'fingerprint_data']
    can_delete = False 
    extra = 0  
class ClassAdmin(admin.ModelAdmin):
    list_display = ['class_name', 'teacher', 'student_count', ]
    inlines = [StudentInline]
    def student_count(self, obj):
        return obj.student_count()
    student_count.short_description = 'Class Size'
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'formatted_timestamp']
    def formatted_timestamp(self, obj):
        local_timestamp = localtime(obj.timestamp) 
        return local_timestamp.strftime('%Y-%m-%d %H:%M:%S')
    formatted_timestamp.short_description = 'Thời gian điểm danh'
    formatted_timestamp.admin_order_field = 'timestamp'

# Đăng ký các mô hình vào Admin
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Class, ClassAdmin)  
admin.site.register(Attendance, AttendanceAdmin)
