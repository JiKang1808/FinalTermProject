# Generated by Django 5.1.1 on 2024-11-12 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0013_remove_attendance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Thời gian điểm danh'),
        ),
    ]