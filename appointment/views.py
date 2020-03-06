from django.views.decorators.http import require_http_methods
from rest_framework.decorators import permission_classes, api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, viewsets
from django.http import Http404, JsonResponse
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
import uuid
import boto
from boto.s3.key import Key
import json


from doctor.models import Doctor
from client.models import Client
from assistant.permissions import IsAssistantUser
from doctor.permissions import IsDoctorUser
from client.permissions import IsClientUser
from authservice.models import RoleType


from .models import Appointment, AppointmentStatus, DoctorShareRecord, Record, Feedback
from .serializer import AppointmentSerializer,\
    RecordSerializer,\
    DoctorShareRecordSerializer,\
    FeedbackSerializer
from .exceptions import AppointmentExistsException, \
    AppointmentStartDateException, \
    AppointmentEndDateException


def validate_appointment(new_data):
    appointments = Appointment.objects.filter(appointment_date=new_data['appointment_date'])
    if new_data['appointment_date'] < timezone.now():
        raise AppointmentStartDateException()

    if new_data['appointment_date'] >= timezone.now() + timedelta(days=7):
        raise AppointmentEndDateException()

    for appointment in appointments:
        if appointment.start_time <= new_data['start_time'] <= appointment.end_time \
                and appointment.status == AppointmentStatus.Created:
            raise AppointmentExistsException()

        if appointment.start_time <= new_data['end_time'] <= appointment.end_time \
                and appointment.status == AppointmentStatus.Created:
            raise AppointmentExistsException()


class AppointmentAssistantList(APIView):
    @permission_classes((IsAuthenticated, IsAssistantUser))
    def get(self, request):
        doctors = Appointment.objects.filter(assistant__user=request.user)
        serializer = AppointmentSerializer(doctors, many=True)
        return Response(serializer.data)

    @permission_classes((IsAuthenticated, IsAssistantUser))
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_data = serializer.validated_data

        validate_appointment(new_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AppointmentList(APIView):
    @permission_classes((IsAuthenticated, IsDoctorUser))
    def get(self, request):
        doctors = Appointment.objects.filter(doctor__user=request.user)
        serializer = AppointmentSerializer(doctors, many=True)
        return Response(serializer.data)


class AppointmentAssistantDetail(APIView):
    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404

    @permission_classes((IsAuthenticated, IsAssistantUser))
    def get(self, request, pk, format=None):
        appointment = self.get_object(pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    @permission_classes((IsAuthenticated, IsAssistantUser))
    def put(self, request, pk, format=None):
        appointment = self.get_object(pk)
        if not appointment.assistant.user == request.user:
            raise ValidationError("You don't have permissions to update this appointment")
        serializer = AppointmentSerializer(appointment, data=request.data)
        serializer.is_valid(raise_exception=True)
        new_data = serializer.validated_data

        validate_appointment(new_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AppointmentDetail(APIView):
    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404

    @permission_classes((IsAuthenticated, IsDoctorUser))
    def get(self, request, pk, format=None):
        appointment = self.get_object(pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)


@csrf_exempt
@permission_classes((IsAuthenticated, IsDoctorUser, IsClientUser))
@api_view(["POST"])
def get_appointment_records(request):
    print("in herere")
    load_data = json.loads(request.body)
    client_id = load_data.get("client")
    doctor_id = load_data.get("doctor")
    appointment_id = load_data.get("appointment")

    if appointment_id is None:
        raise ValidationError("appointment id required")

    if not Appointment.objects.filter(id=appointment_id).exists():
        raise ValidationError("Invalid appointment id")

    if client_id is None:
        raise ValidationError("client id required")

    if not Client.objects.filter(id=client_id).exists():
        raise ValidationError("Invalid client id")

    if doctor_id is None:
        raise ValidationError("doctor id required")

    if not Doctor.objects.filter(id=doctor_id).exists():
        raise ValidationError("Invalid doctor id")

    doctor = Doctor.objects.get(id=doctor_id)
    client = Client.objects.get(id=client_id)

    print("test")
    print(request.user)
    print(client.user)

    if request.user.role == RoleType.Doctor:
        if not request.user == doctor.user:
            raise ValidationError("You don't not have access to update this data")

    if request.user.role == RoleType.Client:
        if not request.user == client.user:
            raise ValidationError("You don't not have access to update this data")


    records = Record.objects.filter(client=client, appointment__doctor=doctor, is_revoked=False)

    records = [{"client": record.client.id, "id": record.id, "appointment": record.appointment.id, "record_url": record.record_url} for record in records]

    return JsonResponse(records, safe=False)


class UploadRecordView(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    parser_classes = (FormParser, MultiPartParser)

    def save_document(self, content, appointment_id, client_id):
        conn = boto.connect_s3(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        bucket_name = settings.AWS_S3_ACCOUNTS_BUCKET
        bucket = conn.get_bucket(bucket_name, validate=False)

        doc_id = str(uuid.uuid4())
        full_key = "{}/{}/{}".format(client_id, appointment_id, doc_id)
        k = Key(bucket)
        k.key = full_key
        k.set_contents_from_file(content, headers={'Content-Type': 'application/zip'})
        return doc_id

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        file_obj = serializer.validated_data['file']
        appointment = serializer.validated_data['appointment']
        client = serializer.validated_data['client']

        if appointment is None:
            raise ValidationError("Please pass appointment id")

        if not Client.objects.filter(id=client.id).exists():
            raise ValidationError("Invalid Client id")

        if not Appointment.objects.filter(id=appointment.id).exists():
            raise ValidationError("Invalid Appointment id")

        if Record.objects.filter(client=client.id, appointment=appointment.id).exists():
            raise ValidationError("Already have a record for this appointment")

        doc_id = self.save_document(file_obj, appointment.id, client.id)
        serializer.save(doc_id=doc_id)

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        file_obj = serializer.validated_data['file']
        appointment = serializer.validated_data['appointment']
        client = serializer.validated_data['client']

        if appointment is None:
            raise ValidationError("Please pass appointment id")

        if not Client.objects.filter(id=client.id).exists():
            raise ValidationError("Invalid Client id")

        if not Appointment.objects.filter(id=appointment.id).exists():
            raise ValidationError("Invalid Appointment id")

        doc_id = self.save_document(file_obj, appointment.id, client.id)
        serializer.save(doc_id=doc_id)


@csrf_exempt
@permission_classes((IsAuthenticated, IsClientUser))
@api_view(["POST"])
def revoke_record_access(request):
    load_data = json.loads(request.body)
    appointment = load_data.get("appointment")
    client = load_data.get("client")
    record = load_data.get("record")

    if appointment is None:
        raise ValidationError("appointment id required")

    if not Appointment.objects.filter(id=appointment).exists():
        raise ValidationError("Invalid appointment id")

    if client is None:
        raise ValidationError("client id required")

    if not Client.objects.filter(id=client).exists():
        raise ValidationError("Invalid client id")

    if record is None:
        raise ValidationError("record id required")

    if not Record.objects.filter(id=record).exists():
        raise ValidationError("Invalid record id")

    client = Client.objects.get(id=client)

    if not request.user == client.user:
        raise ValidationError("You don't not have access to update this")

    record = Record.objects.get(client=client, appointment=appointment, id=record)

    record.is_revoked = True
    record.save()

    return JsonResponse({"message": "Successully revoked"}, safe=False)


class DoctorShareRecordList(APIView):
    @permission_classes((IsAuthenticated, IsClientUser, IsDoctorUser))
    def get(self, request):
        if request.user.role == RoleType.Doctor:
            shared_records = DoctorShareRecord.objects.filter(doctor__user=request.user, record__is_revoked=False)
        else:
            shared_records = DoctorShareRecord.objects.filter(client__user=request.user, record__is_revoked=False)

        serializer = DoctorShareRecordSerializer(shared_records, many=True)
        return Response(serializer.data)

    @permission_classes((IsAuthenticated, IsClientUser))
    def post(self, request):
        serializer = DoctorShareRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_data = serializer.validated_data


        print("data")
        print(new_data)
        if not Doctor.objects.filter(id=new_data['doctor'].id).exists():
            raise ValidationError("Invalid doctor id")

        if not Client.objects.filter(id=new_data['client'].id).exists():
            raise ValidationError("Invalid client id")

        if not Record.objects.filter(id=new_data['record'].id).exists():
            raise ValidationError("Invalid record id")

        if Record.objects.get(id=new_data['record'].id).is_revoked:
            raise ValidationError("Record has been revoked by the client")

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DoctorShareRecordDetail(APIView):

    permission_classes = (IsAuthenticated, IsDoctorUser, IsClientUser)

    def get_object(self, pk):
        try:
            return DoctorShareRecord.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        shared_record = self.get_object(pk)
        serializer = AppointmentSerializer(shared_record)
        return Response(serializer.data)


class FeedbackList(APIView):
    @permission_classes((IsAuthenticated, ))
    def get(self, request):
        feedbacks = Feedback.objects.all()
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

    @permission_classes((IsAuthenticated, IsClientUser))
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_data = serializer.validated_data

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FeedbackDetail(APIView):
    def get_object(self, pk):
        try:
            return Feedback.objects.get(pk=pk)
        except Feedback.DoesNotExist:
            raise Http404

    @permission_classes((IsDoctorUser, IsClientUser, IsAssistantUser, IsAuthenticated))
    def get(self, request, pk, format=None):
        feedback = self.get_object(pk)
        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data)

    @permission_classes((IsClientUser, IsAuthenticated))
    def put(self, request, pk, format=None):
        feedback = self.get_object(pk)
        serializer = FeedbackSerializer(feedback, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








