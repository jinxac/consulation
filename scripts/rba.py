import django
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

GROUPS = ['doctor', 'assistant', 'client']

for group in GROUPS:
    new_group, created = Group.objects.get_or_create(name=group)


def create_doctor_permissions():
    content_type = ContentType.objects.get(app_label='doctor', model='Doctor')
    doctor_group = Group.objects.get(name='doctor')

    permission_list = [
        ('can_view_record', 'Can view Record'),
        ('can_view_appointment', 'Can view Appointment')
    ]

    for p in permission_list:
        permission = Permission.objects.create(
            codename=p[0],
            name=p[1],
            content_type=content_type
        )
        doctor_group.permissions.add(permission)


def create_assistant_permissions():
    content_type = ContentType.objects.get(app_label='assistant', model='Assistant')
    assistant_group = Group.objects.get(name='assistant')

    permission_list = [
        ('can_add_appointment', 'Can add Appointment'),
        ('can_update_appointment', 'Can update Appointment'),
        ('can_view_appointment', 'Can view Appointment')
    ]

    for p in permission_list:
        permission = Permission.objects.create(
            codename=p[0],
            name=p[1],
            content_type=content_type
        )
        assistant_group.permissions.add(permission)


def create_client_permissions():
    content_type = ContentType.objects.get(app_label='client', model='Client')
    client_group = Group.objects.get(name='client')

    permission_list = [
        ('can_add_record', 'Can add record'),
        ('can_update_record', 'Can update record'),
        ('can_view_appointment', 'Can view Appointment'),
        ('can_share_record', 'Can share record')
    ]

    for p in permission_list:
        permission = Permission.objects.create(
            codename=p[0],
            name=p[1],
            content_type=content_type
        )
        client_group.permissions.add(permission)


create_doctor_permissions()
create_assistant_permissions()
create_client_permissions()




