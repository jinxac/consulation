from commons.models.serializer import LogicalDeleteModelSerializer
from .models import Appointment
from .models import Record
from .models import DoctorShareRecord


class AppointmentSerializer(LogicalDeleteModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class RecordSerializer(LogicalDeleteModelSerializer):
    class Meta:
        model = Record
        fields = "__all__"


class DoctorShareRecordSerializer(LogicalDeleteModelSerializer):
    class Meta:
        model = DoctorShareRecord
        fields = "__all__"




