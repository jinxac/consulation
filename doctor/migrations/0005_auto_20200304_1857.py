# Generated by Django 3.0.3 on 2020-03-04 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0004_auto_20200303_0729'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctor',
            options={'permissions': [('change_task_status', 'Can change the status of tasks'), ('close_task', 'Can remove a task by setting its status as closed')]},
        ),
    ]
