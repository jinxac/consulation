from commons.models.serializer import LogicalDeleteModelSerializer
from .models import Client


class ClientSerializer(LogicalDeleteModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
        read_only_fields = ['user']
