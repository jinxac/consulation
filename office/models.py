from django.db import models

from commons.models.models import LogicalDeleteModel

from doctor.models import Doctor
from assistant.models import Assistant


class Office(LogicalDeleteModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)
    time_slot_per_client_in_minutes = models.IntegerField()
    first_consultation_fee = models.DecimalField(max_digits=20, decimal_places=6)
    follow_up_consultation_fee = models.DecimalField(max_digits=20, decimal_places=6)
    street_address = models.CharField(max_length=300)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip = models.IntegerField()


class OfficeDoctorAvailability(LogicalDeleteModel):
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    day_of_week = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField()
    reason_of_unavailability = models.CharField(max_length=255)


class OfficeInsurance(LogicalDeleteModel):
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    insurance_name = models.CharField(max_length=255)
