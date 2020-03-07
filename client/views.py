from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from .models import Client
from .serializer import ClientSerializer
from .permissions import IsClientUser
from rest_framework.exceptions import ValidationError

from doctor.permissions import IsDoctorUser
from assistant.permissions import IsAssistantUser

from authservice.models import RoleType


class ClientList(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser | IsClientUser | IsDoctorUser | IsAssistantUser)

    def get(self, request):
        if request.user.role == RoleType.Client:
            clients = Client.objects.filter(user=request.user)
        else:
            clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)


class ClientDetail(APIView):
    permission_classes = (IsAuthenticated,  IsAdminUser | IsClientUser | IsDoctorUser | IsAssistantUser)

    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        client = self.get_object(pk)
        if request.user.role == RoleType.Client and not request.user == client.user:
            raise ValidationError("You do not have permission to access this data")
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        client = self.get_object(pk)
        if not client.user == request.user:
            raise ValidationError("Cannot update info for this user")
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

