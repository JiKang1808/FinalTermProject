# attendance/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Teacher, Student

@receiver(post_save, sender=User)
def create_teacher_or_student(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'Teacher':
            Teacher.objects.create(user=instance, name=instance.username)
        elif instance.role == 'Student':
            Student.objects.create(user=instance, name=instance.username)
