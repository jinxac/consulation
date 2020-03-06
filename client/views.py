from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from .models import Client
from .serializer import ClientSerializer
from .permissions import IsClientUser
from assistant.permissions import IsAssistantUser
from doctor.permissions import IsDoctorUser
from rest_framework.exceptions import ValidationError


class ClientList(APIView):
    permission_classes = (IsAuthenticated, IsClientUser)

    def get(self, request):
        clients = Client.objects.filter(user=request.user)
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)


class ClientDetail(APIView):
    permission_classes = (IsAuthenticated, IsClientUser)

    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        client = self.get_object(pk)
        if not request.user == client.user:
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

