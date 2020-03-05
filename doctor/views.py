from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Doctor
from .serializer import DoctorSerializer
from rest_framework.exceptions import ValidationError


class DoctorList(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)


class DoctorDetail(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        doctor = self.get_object(pk)
        if not doctor.user == request.user:
            raise ValidationError("You cannot access this information")
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        doctor = self.get_object(pk)
        if not doctor.user == request.user:
            raise ValidationError("You don't have access to update this user")

        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

