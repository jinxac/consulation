from django.db import models

from commons.models.models import LogicalDeleteModel

from authservice.models import User
from .manager import AssistantManager


class Assistant(LogicalDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = AssistantManager()
