from django.db import models

from commons.models.models import LogicalDeleteModel


class Assistant(LogicalDeleteModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateTimeField()
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=255)
