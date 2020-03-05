from rest_framework import serializers

from commons.models.serializer import LogicalDeleteModelSerializer
from .models import Appointment
from .models import Record
from .models import DoctorShareRecord
from .models import Feedback


class AppointmentSerializer(LogicalDeleteModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class RecordSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = Record
        fields = ['id', 'client', 'doc_id', 'appointment', 'file', 'record_url']

    def create(self, validated_data):
        validated_data.pop("file", None) #popping data not required
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("file", None) #popping data not required
        return super().create(validated_data)


class DoctorShareRecordSerializer(LogicalDeleteModelSerializer):
    class Meta:
        model = DoctorShareRecord
        fields = "__all__"


class FeedbackSerializer(LogicalDeleteModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"



