import django
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from authservice.models import User, RoleType

from doctor.models import Doctor
from assistant.models import Assistant
from client.models import Client
from office.models import Office

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


def create_users():
    users = [
        {
            "email": "doctor1@gmail.com",
            "password": "12345678",
            "first_name": "James",
            "last_name": "Brin",
            "phone_number": "9886268121",
            "role": 0
        },
        {
            "email": "doctor2@gmail.com",
            "password": "12345678",
            "first_name": "James",
            "last_name": "Lebron",
            "phone_number": "9886268123",
            "role": 0
        },
        {
            "email": "doctor3@gmail.com",
            "password": "12345678",
            "first_name": "Virat",
            "last_name": "Kohli",
            "phone_number": "9886268124",
            "role": 0
        },
        {
            "email": "assistant1@gmail.com",
            "password": "12345678",
            "first_name": "Rupesh",
            "last_name": "Bansal",
            "phone_number": "9886268122",
            "role": 1
        },
        {
            "email": "assistant2@gmail.com",
            "password": "12345678",
            "first_name": "Rahul",
            "last_name": "Saturn",
            "phone_number": "9886268123",
            "role": 1
        },
        {
            "email": "assistant3@gmail.com",
            "password": "12345678",
            "first_name": "Rajesh",
            "last_name": "Kumar",
            "phone_number": "9886268124",
            "role": 1
        },
        {
            "email": "client1@gmail.com",
            "password": "12345678",
            "first_name": "Neha",
            "last_name": "Chugh",
            "phone_number": "9886268122",
            "role": 2
        },
        {
            "email": "client2@gmail.com",
            "password": "12345678",
            "first_name": "Harkirat",
            "last_name": "Saluja",
            "phone_number": "9886268123",
            "role": 2
        },
        {
            "email": "client3@gmail.com",
            "password": "12345678",
            "first_name": "Manoj",
            "last_name": "Kumar",
            "phone_number": "9886268124",
            "role": 2
        },
    ]

    for user in users:
        entity = User.objects.create(**user)
        entity.is_active = True
        entity.set_password(user['password'])
        entity.save()

        if entity.role == RoleType.Doctor:
            Doctor.objects.create_user(user=entity)
            group_1 = Group.objects.get(name='doctor')
            entity.groups.add(group_1)

        if entity.role == RoleType.Assistant:
            Assistant.objects.create_user(user=entity)
            group_1 = Group.objects.get(name='assistant')
            entity.groups.add(group_1)

        if entity.role == RoleType.Client:
            Client.objects.create_user(user=entity)
            group_1 = Group.objects.get(name='client')
            entity.groups.add(group_1)

mock_data = [
    {
        "name": "Test Clinic 1",
        "street_address": "First Street Address",
        "city": "Bangalore",
        "state": "Karnataka",
        "country": "India",
        "zip": 560102
    },
    {
        "name": "Test Clinic 2",
        "street_address": "Second Street Address",
        "city": "Bangalore",
        "state": "Karnataka",
        "country": "India",
        "zip": 560102
    },
    {
        "name": "Test Clinic 3",
        "street_address": "Third Street Address",
        "city": "Bangalore",
        "state": "Karnataka",
        "country": "India",
        "zip": 560102
    }
]


def create_office():
    for datum in mock_data:
        Office.objects.create(
            name=datum['name'],
            street_address=datum['street_address'],
            city=datum['city'],
            state=datum['state'],
            country=datum['country'],
            zip=datum['zip']
        )


create_doctor_permissions()
create_assistant_permissions()
create_client_permissions()
create_office()

create_users()





