from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializer import UserSignupSerializer


class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = (
        permissions.AllowAny,
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data["email"] = validated_data["email"].lower()

        serializer.save()

        resp = {"success": "User has been created"}
        return Response(resp, status=status.HTTP_201_CREATED, headers={})
