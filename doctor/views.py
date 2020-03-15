from django.db.transaction import atomic
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Doctor, DoctorAvailability
from .serializer import DoctorSerializer
from rest_framework.exceptions import ValidationError
from .permissions import IsDoctorUser
from assistant.permissions import IsAssistantUser

import json
from datetime import datetime
from datetime import time
from django.views.decorators.csrf import csrf_exempt


class DoctorList(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)


class DoctorDetail(APIView):
    permission_classes = (IsAuthenticated, IsDoctorUser)

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


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated, IsAssistantUser))
def update_doctor_availability(request):
    load_data = json.loads(request.body)
    doctor_id = load_data.get("doctor")
    start_time = load_data.get("start_time")
    end_time = load_data.get("end_time")


    if doctor_id is None:
        raise ValidationError("doctor id required")


    if start_time is None:
        raise ValidationError("start time required")

    if end_time is None:
        raise ValidationError("start time required")

    if end_time < start_time:
        raise ValidationError("end time should be less than start time required")

    # if start_time < time():
    #     raise ValidationError("start time should be after now")
    #
    # if end_time < time():
    #     raise ValidationError("end time should be after now")


    if not Doctor.objects.filter(id=doctor_id).exists():
        raise ValidationError("Invalid doctor id")

    doctor = Doctor.objects.get(id=doctor_id)
    DoctorAvailability.objects.create(
        doctor=doctor,
        day_of_week=datetime.today().weekday(),
        start_time=start_time,
        end_time=end_time
    )

    return JsonResponse({"message": "Successfully created"}, safe=False)