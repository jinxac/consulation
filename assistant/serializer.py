from commons.models.serializer import LogicalDeleteModelSerializer
from .models import Assistant


class AssistantSerializer(LogicalDeleteModelSerializer):
    class Meta:
        model = Assistant
        fields = "__all__"
        read_only_fields = ['user']
