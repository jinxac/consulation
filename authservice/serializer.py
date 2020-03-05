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
            Assistant.objects.create_user(user=user)
            assistant_group = Group.objects.get(name='assistant')
            user.groups.add(assistant_group)

        if user.role == RoleType.Doctor:
            Doctor.objects.create_user(user=user)
            doctor_group = Group.objects.get(name='doctor')
            user.groups.add(doctor_group)
        if user.role == RoleType.Client:
            Client.objects.create_user(user=user)
            assistant_group = Group.objects.get(name='client')
            user.groups.add(assistant_group)

        return user
