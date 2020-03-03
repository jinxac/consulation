from commons.models.serializer import LogicalDeleteModelSerializer
from .models import Office


class OfficeSerializer(LogicalDeleteModelSerializer):
    class Meta:
        model = Office
        fields = "__all__"
