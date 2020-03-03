from django.db import models
from django.utils import timezone

from datetime import timedelta

from commons.models.models import LogicalDeleteModel
from authservice.models import User
from office.models import Office

from .manager import DoctorManager


class Specialization(LogicalDeleteModel):
    specialization_name = models.CharField(max_length=100)


class Doctor(LogicalDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    professional_statement = models.CharField(max_length=300, null=True, blank=True)
    practicing_from = models.DateTimeField(blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=20, decimal_places=6)
    avg_consultation_time = models.DurationField(default=timedelta(minutes=30))

    specialization = models.CharField(max_length=255)

    objects = DoctorManager()

    @property
    def experience(self):
        if not self.practicing_from:
            return 0
        return timezone.now().year - self.practicing_from.year


class DoctorAvailability(LogicalDeleteModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day_of_week = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

# TODO: Can extend feature to add multiple specializations
# specializations = models.ManyToManyField(Specialization, through='DoctorSpecialization', blank=True)
# class DoctorSpecialization(LogicalDeleteModel):
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)


# class Qualification (LogicalDeleteModel):
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     qualification_name = models.CharField(max_length=100)
#     institute_name = models.CharField(max_length=100)
#     procurement_year = models.DateTimeField()






