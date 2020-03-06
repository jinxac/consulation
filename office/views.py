from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Office
from .serializer import OfficeSerializer

from doctor.permissions import IsDoctorUser


class OfficeList(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        doctors = Office.objects.all()
        serializer = OfficeSerializer(doctors, many=True)
        return Response(serializer.data)


class OfficeDetail(APIView):

    def get_object(self, pk):
        try:
            return Office.objects.get(pk=pk)
        except Office.DoesNotExist:
            raise Http404

    @permission_classes((IsAuthenticated, IsAdminUser))
    def get(self, request, pk, format=None):
        office = self.get_object(pk)
        serializer = OfficeSerializer(office)
        return Response(serializer.data)

    @permission_classes((IsAuthenticated))
    def put(self, request, pk, format=None):
        office = self.get_object(pk)
        serializer = OfficeSerializer(office, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

