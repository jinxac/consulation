from django.db import models
import boto3
from django.conf import settings
from botocore.exceptions import ClientError
from boto.s3.connection import S3Connection

from commons.models.models import LogicalDeleteModel
from rest_framework.exceptions import ValidationError


from doctor.models import Doctor
from client.models import Client


class AppointmentStatus(models.IntegerChoices):
    Created = 0
    Completed = 1
    Cancelled = 2


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

# TODO: Can move to utils in future
# def get_upload_url(full_key):
#     s3_client = boto3.client(
#         "s3",
#         aws_access_key_id=settings.AWS_ACCESS_KEY,
#         aws_secret_access_key=settings.AWS_SECRET_KEY,
#     )
#     try:
#         response = s3_client.generate_presigned_post(
#             settings.AWS_S3_ACCOUNTS_BUCKET, full_key, ExpiresIn=1800
#         )
#     except ClientError as e:
#         raise ValidationError(e)
#     return response


class Appointment(LogicalDeleteModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    appointment_date = models.DateTimeField()
    status = models.IntegerField(choices=AppointmentStatus.choices)


class Record(LogicalDeleteModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    doc_id = models.CharField(max_length=255, null=True, blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True)
    is_revoked = models.BooleanField(default=False)

    @property
    def record_url(self):
        full_key = "{}/{}".format(
            self.client.id, self.doc_id
        )
        return get_image_signed_url(full_key)


class DoctorShareRecord(LogicalDeleteModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class Feedback(LogicalDeleteModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField()
    rating = models.IntegerField()
    description = models.CharField(max_length=255)


