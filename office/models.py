from django.db import models

from commons.models.models import LogicalDeleteModel


class Office(LogicalDeleteModel):
    street_address = models.CharField(max_length=300)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip = models.IntegerField()
