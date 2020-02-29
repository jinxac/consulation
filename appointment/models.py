from django.db import models

from commons.models.models import LogicalDeleteModel


from office.models import Office
from client.models import Client


class AppointmentStatus(models.IntegerChoices):
    Created = 0
    Active = 1
    Cancelled = 2


class Appointment(LogicalDeleteModel):
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    probable_start_time = models.DateTimeField()
    actual_start_time = models.DateTimeField()
    actual_end_time = models.DateTimeField()
    status = models.IntegerField(choices=AppointmentStatus.choices)
    appointment_date = models.DateTimeField()

