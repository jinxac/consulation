from django.db import models

from commons.models.models import LogicalDeleteModel


from doctor.models import Doctor
from client.models import Client


class AppointmentStatus(models.IntegerChoices):
    Created = 0
    Completed = 1
    Cancelled = 2


# TODO: Move to utils
def get_upload_url(full_key):
    print(full_key)
    # TODO: Add logic to upload the doc


class Appointment(LogicalDeleteModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    appointment_date = models.DateTimeField()
    status = models.IntegerField(choices=AppointmentStatus.choices)


class Record(LogicalDeleteModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doc_id = models.CharField(max_length=255, null=True, blank=True)

    @property
    def record_url(self):
        full_key = "{}/{}".format(
            self.client.id, self.doc_id
        )
        return get_upload_url(full_key)


class Feedback(LogicalDeleteModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField()
    rating = models.IntegerField()
    description = models.CharField(max_length=255)


