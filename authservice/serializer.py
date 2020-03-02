from rest_framework import serializers
from django.db import transaction

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
        user.save()
        if user.role == RoleType.Assistant:
            # TODO: Later assign permissions here
            Assistant.objects.create_user(user=user)
        if user.role == RoleType.Doctor:
            # TODO: Later assign permissions here
            Doctor.objects.create_user(user=user)
        if user.role == RoleType.Client:
            # TODO: Later assign permissions here
            Client.objects.create_user(user=user)
        return user
