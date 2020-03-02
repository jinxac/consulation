from rest_framework import serializers
from django.db import transaction

from authservice.models import User, RoleType
from authservice.exceptions import EmailAlreadyRegisteredException


class UserSignupSerializer(serializers.Serializer):

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
        return user
