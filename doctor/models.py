from django.db import models


from commons.models.models import LogicalDeleteModel
from authservice.models import User

from .manager import DoctorManager


class Specialization(LogicalDeleteModel):
    specialization_name = models.CharField(max_length=100)


class Doctor(LogicalDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    professional_statement = models.CharField(max_length=300, null=True, blank=True)
    practicing_from = models.DateTimeField(blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    specializations = models.ManyToManyField(Specialization, through='DoctorSpecialization', blank=True)
    objects = DoctorManager()


class DoctorSpecialization(LogicalDeleteModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Qualification (LogicalDeleteModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    qualification_name = models.CharField(max_length=100)
    institute_name = models.CharField(max_length=100)
    procurement_year = models.DateTimeField()






