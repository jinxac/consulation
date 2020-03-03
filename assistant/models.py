from django.db import models

from commons.models.models import LogicalDeleteModel
from authservice.models import User
from office.models import Office

from .manager import AssistantManager


class Assistant(LogicalDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True)

    objects = AssistantManager()
