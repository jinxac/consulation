from commons.models.serializer import LogicalDeleteModelSerializer
from .models import Doctor


class DoctorSerializer(LogicalDeleteModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"
        read_only_fields = ['user']
