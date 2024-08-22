import django
from django.dispatch import receiver

from attendance.models import AttendanceHistory


attendance_taken_signal = django.dispatch.Signal(providing_args=["date", "present", "absent", "stream"])


@receiver(attendance_taken_signal)
def receive_attendance_taken(date, present, absent, stream, **kwargs):
    # print("REceived the signal")
    # print(date, present, absent, stream)
    id = date.replace('-', '') + "%s" % (stream)
    # print(id)
    at = AttendanceHistory(id=id, present=present, stream_id=stream, absent=absent, date=date)
    at.save()
