from django.db import models
from django.conf import settings
from boto.s3.connection import S3Connection

from commons.models.models import LogicalDeleteModel
from rest_framework.exceptions import ValidationError


from doctor.models import Doctor
from client.models import Client
from assistant.models import Assistant


class AppointmentStatus(models.IntegerChoices):
    Created = 0
    Completed = 1
    Cancelled = 2


# TODO: Can move to utils in future
def get_image_signed_url(full_key, https=True, expiry=1800):
    if not full_key:
        raise ValidationError("Invalid doc id")

    c = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
    return c.generate_url(
        expires_in=expiry,
        method='GET',
        bucket=settings.AWS_S3_ACCOUNTS_BUCKET,
        key=full_key,
        query_auth=True,
        force_http=(not https)
    )


class Appointment(LogicalDeleteModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    appointment_date = models.DateField()
    status = models.IntegerField(choices=AppointmentStatus.choices)


class Record(LogicalDeleteModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    doc_id = models.CharField(max_length=255, null=True, blank=True)
    # TODO: Can be made one to one, for now kept it flexible
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True)
    is_revoked = models.BooleanField(default=False)

    @property
    def record_url(self):
        full_key = "{}/{}/{}".format(
            self.client.id, self.appointment.id, self.doc_id
        )
        return get_image_signed_url(full_key)


class DoctorShareRecord(LogicalDeleteModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class Feedback(LogicalDeleteModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    # TODO: Can be made one to one, kept it flexible for now
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)
    rating = models.IntegerField()
    description = models.CharField(max_length=255)


