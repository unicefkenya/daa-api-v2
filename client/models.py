from __future__ import unicode_literals

from datetime import timedelta

import sys
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.timezone import now

from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill, ResizeToFit


from mylib.image import scramble
from oauth2_provider.models import AccessToken, Application
from oauthlib.common import generate_token

from mylib.my_common import MySendEmail
from wvapi.settings import MY_SITE_URL
from django.contrib.auth import get_user_model


def get_user_by_id(claimss, two):
    print(claimss, two)
    return get_user_model().objects.first()


class UserMixin(models.Model):
    last_activity = models.DateTimeField(default=timezone.now, editable=False)

    def update_last_activity(self):
        self.last_activity = timezone.now()
        self.save(update_fields=["last_activity"])

    class Meta:
        abstract = True


SCHOOL_ADMIN = "SCHA"
SCHOOL_TEACHER = "SCHT"
SUB_COUNTY_ADMIN = "SCO"
COUNTY_ADMIN = "CO"




class MyUser(UserMixin, AbstractUser):
    ROLES = (
        ("A", "Admin"),
        (SCHOOL_ADMIN, "School Admin"),  ## User params id is a school //should be a school object instead
        (SCHOOL_TEACHER, "School Teacher"),  ##
        (COUNTY_ADMIN, "County Officer"),
        (SUB_COUNTY_ADMIN, "Sub County Officer"),
        ("RO", "Read Only"),
    )
    SEX = (("M", "Male"), ("F", "Female"), ("NS", "Not Set"))
    # TYPE=(('AT','Attendee'),('OG','Organizer'))
    role = models.CharField(max_length=45, default="A", choices=ROLES)
    phone = models.CharField(max_length=50, null=True, blank=True)
    google_profile_image = models.URLField(max_length=200, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField("uploads", upload_to=scramble, null=True, blank=True)
    gender = models.CharField(max_length=5, choices=SEX, default="NS")
    allow_notification = models.BooleanField(default=True)
    main_image = ImageSpecField(source="image", processors=[ResizeToFit(height=400)], format="JPEG", options={"quality": 80})
    confirm_code = models.IntegerField(null=True, blank=True)
    reset_code = models.IntegerField(null=True, blank=True)
    old_password = models.CharField(null=True, blank=True, max_length=55)
    changed_password = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    dummy = models.BooleanField(default=False)
    filter_args = models.CharField(null=True, blank=True, max_length=1000)
    is_partner=models.BooleanField(default=False)
    
    
    
    

    class Meta:
        ordering = ("id",)

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    # def save(self, *args, **kwargs):
    #     self.password = make_password(self.password)
    #     super(MyUser, self).save(*args, **kwargs)
    # bookings=models.


class ActivityLog(models.Model):
    user = models.ForeignKey(MyUser, null=True, blank=True, on_delete=models.CASCADE)
    request_url = models.URLField(max_length=256)
    request_method = models.CharField(max_length=10)
    response_code = models.CharField(max_length=3)
    datetime = models.DateTimeField(default=timezone.now)
    # username=models.
    device = models.CharField(max_length=1000, null=True, blank=True)
    browser = models.CharField(max_length=1000, null=True, blank=True)
    os = models.CharField(max_length=1000, null=True, blank=True)
    extra_data = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ("-id",)


# class Client(AbstractUser):
#     id = models.CharField(primary_key=True ,max_length=20)
#     phone = models.CharField(max_length=20,null=True,blank=True)


@receiver(post_save, sender=MyUser, dispatch_uid="my_unique_identifier")
def my_user_handler(sender, **kwargs):
    created = kwargs["created"]
    instance = kwargs["instance"]

    if created and "test" not in sys.argv:
        # return
        ##Send email
        user = instance
        token = generate_token()
        app = Application.objects.first()
        AccessToken.objects.create(user=user, application=app, expires=now() + timedelta(days=1), token=token)
        link = "%s/verify-account?token=%s&confirm_code=%s" % (MY_SITE_URL, token, instance.confirm_code)
        data = {"name": user.first_name, "verify_url": link, "old_password": instance.old_password}
        instance.old_password = None
        instance.save()

        if user.email == None or user.email == "":
            return
        try:
            MySendEmail("Onekana Digital Attendance", "new_user.html", data, [user.email])
            instance.old_password = ""
            instance.save()
        except Exception as e:
            print(e)
            pass
