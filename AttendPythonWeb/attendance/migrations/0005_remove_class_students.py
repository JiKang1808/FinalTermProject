# Generated by Django 5.1.2 on 2024-10-27 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_class_students'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='students',
        ),
    ]
