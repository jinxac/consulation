from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.views.decorators.http import require_http_methods
from rest_framework.exceptions import ValidationError
import uuid
import boto
from boto.s3.key import Key

from doctor.models import Doctor
from client.models import Client

from .models import Appointment, AppointmentStatus, DoctorShareRecord, Record
from .serializer import AppointmentSerializer,\
    RecordSerializer,\
    DoctorShareRecordSerializer
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
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        doctors = Appointment.objects.all()
        serializer = AppointmentSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_data = serializer.validated_data

        validate_appointment(new_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AppointmentAssistantDetail(APIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        appointment = self.get_object(pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        appointment = self.get_object(pk)
        serializer = AppointmentSerializer(appointment, data=request.data)
        serializer.is_valid(raise_exception=True)
        new_data = serializer.validated_data

        validate_appointment(new_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AppointmentDoctorList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        doctors = Appointment.objects.all()
        serializer = AppointmentSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_data = serializer.validated_data

        validate_appointment(new_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AppointmentDoctorDetail(APIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        appointment = self.get_object(pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)


class UploadRecordView(APIView):
    parser_class = (FileUploadParser,)
    permission_classes = (IsAuthenticated,)

    def create_temp_file(self, size, file_name, file_content):
        random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
        with open(random_file_name, 'w') as f:
            f.write(str(file_content) * size)
        return random_file_name

    def save_document(self, content, content_type="application/zip"):
        conn = boto.connect_s3(aws_access_key_id=settings.AWS_ACCESS_KEY, aws_secret_access_key=settings.AWS_SECRET_KEY)
        bucket_name = settings.AWS_S3_ACCOUNTS_BUCKET
        bucket = conn.get_bucket(bucket_name, validate=False)

        doc_id = str(uuid.uuid4())
        full_key = doc_id
        k = Key(bucket)
        k.key = full_key
        k.set_contents_from_file(content, headers={'Content-Type': 'application/zip'})
        return doc_id

    def post(self, request, format=None):
        serializer = RecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_data = serializer.validated_data
        if 'file' not in request.data:
            raise ParseError("Empty content")

        file = new_data['file']
        doc_id = self.save_document(file)

        return Response(status=status.HTTP_201_CREATED)


class DoctorShareRecordList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        share_records = DoctorShareRecord.objects.all()
        serializer = DoctorShareRecordSerializer(share_records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_data = serializer.validated_data

        if not Doctor.objects.filter(id=new_data.doctor).exists():
            raise ValidationError("Invalid doctor id")

        if not Client.objects.filter(id=new_data.client).exists():
            raise ValidationError("Invalid client id")

        if not Record.objects.filter(id=new_data.record).exists():
            raise ValidationError("Invalid record id")

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DoctorShareRecordDetail(APIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return DoctorShareRecord.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        shared_record = self.get_object(pk)
        serializer = AppointmentSerializer(shared_record)
        return Response(serializer.data)

