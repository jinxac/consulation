from django.db import models

from commons.models.models import LogicalDeleteModel

from authservice.models import User


class Assistant(LogicalDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
