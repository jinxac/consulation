from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.models import Group

from commons.models.serializer import LogicalDeleteModelSerializer
from authservice.models import User, RoleType
from authservice.exceptions import EmailAlreadyRegisteredException
from assistant.models import Assistant
from doctor.models import Doctor
from client.models import Client


class UserSignupSerializer(LogicalDeleteModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type':'password'}, write_only=True, min_length=6)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=15)
    role = serializers.IntegerField()

    class Meta:
        model = User
        fields = "__all__"

    def assign_doctor_to_group(self, user):
        Doctor.objects.create_user(user=user)
        doctor_group = Group.objects.get(name='doctor')
        user.groups.add(doctor_group)

    def assign_assistant_to_group(self, user):
        Assistant.objects.create_user(user=user)
        assistant_group = Group.objects.get(name='assistant')
        user.groups.add(assistant_group)

    def assign_client_to_group(self, user):
        Client.objects.create_user(user=user)
        client_group = Group.objects.get(name='client')
        user.groups.add(client_group)

    @transaction.atomic
    def create(self, validated_data):
        user, is_created = User.objects.get_or_create(email=validated_data['email'])

        if user.is_active:
            raise EmailAlreadyRegisteredException()

        User.objects.filter(email=validated_data["email"]).update(**validated_data)
        user = User.objects.get(email=validated_data["email"])
        user.set_password(validated_data["password"])

        # TODO: Can add email validation with token later
        user.is_active = True
        user.save()

        if user.role == RoleType.Assistant:
            self.assign_assistant_to_group(user)

        if user.role == RoleType.Doctor:
            self.assign_doctor_to_group(user)

        if user.role == RoleType.Client:
            self.assign_client_to_group(user)

        return user
