from django.db import models

from commons.models.models import LogicalDeleteModel
from doctor.models import Doctor
from authservice.models import User


class Record(LogicalDeleteModel):
    record_file = models.CharField(max_length=255)


class Client(LogicalDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    records = models.ForeignKey(Record, on_delete=models.CASCADE)


class Feedback(LogicalDeleteModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField()
    rating = models.IntegerField()
    description = models.CharField(max_length=255)
    review_date = models.DateTimeField()


