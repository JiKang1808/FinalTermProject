# Generated by Django 5.1.2 on 2024-10-27 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_student_user_teacher_user_alter_class_class_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(blank=True, to='attendance.student'),
        ),
    ]
