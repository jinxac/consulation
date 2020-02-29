from django.db import models

from commons.models.models import LogicalDeleteModel
from doctor.models import Doctor


class Record(LogicalDeleteModel):
    record_file = models.CharField(max_length=255)


class Client(LogicalDeleteModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=255)
    records = models.ManyToManyField(Record, through='ClientRecord')


class Feedback(LogicalDeleteModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField()
    rating = models.IntegerField()
    description = models.CharField(max_length=255)
    review_date = models.DateTimeField()


class ClientRecord(LogicalDeleteModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)


