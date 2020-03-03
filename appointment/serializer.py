from commons.models.serializer import LogicalDeleteModelSerializer
from .models import Appointment
from .models import Record


class AppointmentSerializer(LogicalDeleteModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class RecordSerializer(LogicalDeleteModelSerializer):
    class Meta:
        model = Record
        fields = "__all__"





