import sys

from django.db.models.signals import post_save
from django.dispatch import receiver

from mylib.my_common import MySendEmail
from support_question.models import SupportRequest
from support_question.support_requests.serializers import SupportRequestSerializer

SUPPORT_EMAIL="daaonekana@gmail.com"
# SUPPORT_EMAIL="michameiu@gmail.com"


@receiver(post_save, sender=SupportRequest, dispatch_uid="support_question_created")
def my_support_request_handler(sender, **kwargs):
    created = kwargs["created"]
    instance = kwargs["instance"]
    if created:
        if "test" in sys.argv:
            return
        serializer=SupportRequestSerializer(instance)
        subject="#{} {} ({}) - {}".format(instance.id,instance.name,instance.school.name,instance.subject)
        MySendEmail(subject,"support_request.html",serializer.data,[SUPPORT_EMAIL])
