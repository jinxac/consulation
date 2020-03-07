from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from authservice.models import RoleType

from .models import Assistant
from .serializer import AssistantSerializer
from .permissions import IsAssistantUser


from rest_framework.exceptions import ValidationError


class AssistantList(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser | IsAssistantUser, )

    def get(self, request):
        if request.user.role == RoleType.Admin:
            assistants = Assistant.objects.all()
        else:
            assistants = Assistant.objects.filter(user=request.user)

        serializer = AssistantSerializer(assistants, many=True)
        return Response(serializer.data)


class AssistantDetail(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser | IsAssistantUser)

    def get_object(self, pk):
        try:
            return Assistant.objects.get(pk=pk)
        except Assistant.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        assistant = self.get_object(pk)
        if not assistant.user == request.user:
            raise ValidationError("You cannot access this information")
        serializer = AssistantSerializer(assistant)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        assistant = self.get_object(pk)
        if not assistant.user == request.user:
            raise ValidationError("Cannot change info for this user")
        serializer = AssistantSerializer(assistant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


