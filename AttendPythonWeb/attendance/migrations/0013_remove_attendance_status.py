# Generated by Django 5.1.1 on 2024-11-11 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0012_class_start_time_alter_class_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='status',
        ),
    ]
