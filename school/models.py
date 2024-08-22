from os import path

from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.
from django.db.models import F, Value, DateField, Count, Q, CharField
from django.db.models.expressions import RawSQL
from django.db.models.functions import Concat, ExtractMonth, ExtractDay, ExtractYear, Trunc, TruncDate, Coalesce, TruncDay
from django.db.models import Func
from django.utils import timezone
from multiselectfield import MultiSelectField

from client.models import MyUser
from mylib.my_common import case_generator
from mylib.mygenerics import GroupConcat, MyModel
from region.models import Village, SubCounty
from django.utils.dateparse import parse_date
from datetime import date
from django.db.models import Case, When, Value

from django.conf import settings

# from wvapi.settings import MEDIA_ROOT

SPECIAL_NEEDS = (("N", "None"), ("V", "Visual"), ("H", "Hearing"), ("P", "Physical"), ("L", "Learning"))


class School(MyModel):
    LOCATION = (("R", "Rural"), ("U", "Urban"))
    GENDER = (
        ("M", "Boys"),
        ("F", "Girls"),
        ("MX", "Mixed"),
    )
    BOARDING = (("D", "Day Only"), ("B", "Boarding Only"), ("BD", "Boarding and Day"))
    GRADES = (("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"))
    # village = models.ForeignKey(Village, null=True, blank=True, on_delete=models.SET_NULL)
    sub_county = models.ForeignKey(SubCounty, related_name="schools", null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=45)
    emis_code = models.CharField(unique=True, max_length=45)
    phone = models.CharField(null=True, blank=True, max_length=30)
    email = models.EmailField(max_length=100, null=True, blank=True)
    school_ministry = models.CharField(max_length=100, null=True, blank=True)
    founder_name = models.CharField(max_length=70, null=True, blank=True)
    year_of_foundation = models.DateField(null=True, blank=True)
    ownership = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(default="R", max_length=2, choices=LOCATION)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    start_of_calendar = models.DateField(null=True, blank=True)
    end_of_calendar = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    lowest_grade = models.CharField(default="P1", max_length=4, choices=GRADES)
    highest_grade = models.CharField(default="P8", max_length=4, choices=GRADES)
    schooling = models.CharField(default="D", max_length=4, choices=BOARDING)
    gender = models.CharField(default="MX", max_length=4, choices=GENDER)
    moe_id = models.CharField(null=True, blank=True, max_length=50)
    moe_emis_code = models.CharField(null=True, blank=True, max_length=50)
    is_training_school = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("id",)

    @staticmethod
    def get_role_filters():
        return {
            "A": None,
            "SCHA": "id",
            "SCHT": "id",
            "CO": "sub_county__county_id",
            "SCO": "sub_county_id",
        }


SCHOOL_SUB_COUNTY_NAME = F("sub_county__name")
SCHOOL_COUNTY_NAME = F("sub_county__county__name")
SCHOOL_STATS_DEFINITIONS = {
    "id": {
        "value": F("id"),
        "extra_fields": {
            "sub_county_name": SCHOOL_SUB_COUNTY_NAME,
            "county_name": SCHOOL_COUNTY_NAME,
            "day_boarding": F("schooling"),
            "nemis_code": F("emis_code"),
        },
        "resp_fields": {"id", "name", "email", "lat", "lng"},
    },
    "county": {
        "value": F("sub_county__county_id"),
        "extra_fields": {
            "county_name": SCHOOL_COUNTY_NAME,
        },
    },
    "sub-county": {
        "value": F("sub_county_id"),
        "extra_fields": {
            "sub_county_name": SCHOOL_SUB_COUNTY_NAME,
            "county_name": SCHOOL_COUNTY_NAME,
        },
    },
}

DEFAULT_SCHOOL_FIELDS = {}


class SpecialNeed(MyModel):
    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


CLASSES = (("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"))
CLASSES_MAP = {c[0]: c[1] for c in CLASSES}


class Stream(MyModel):
    school = models.ForeignKey(School, related_name="streams", on_delete=models.CASCADE)
    name = models.CharField(max_length=45, default="", null=True, blank=True)
    last_attendance = models.DateField(null=True, blank=True)
    base_class = models.CharField(choices=CLASSES, default="1", max_length=3)
    moe_id = models.CharField(null=True, blank=True, max_length=50)
    moe_section_id = models.CharField(max_length=45, null=True, blank=True)
    moe_name = models.CharField(max_length=45, null=True, blank=True)
    moe_section_name = models.CharField(max_length=45, null=True, blank=True)
    # moe_extra_info=models.JSONField(editable=False,null=True,blank=True)

    @property
    def class_name(self):
        name = self.name if self.name else ""
        return "{} {}".format(CLASSES_MAP[self.base_class], name)

    @property
    def full_class_name(self):
        return "{} - Class {}".format(self.school.name, self.class_name)

    def __str__(self):
        return "CLASS {}".format(self.class_name)

    class Meta:
        ordering = ("id",)
        # unique_together=("school","name")

    @staticmethod
    def get_role_filters():
        return {"A": None, "SCHA": "school_id", "SCHT": "school_id", "CO": "school__sub_county__county_id", "SCO": "school__sub_county_id"}

    def attendance_taken(self, date):
        date = parse_date(date)
        # print("Updating the attendance Date %s"%(date))
        if self.last_attendance == None:
            # print("NO last attendance.")
            self.last_attendance = date
        elif date > self.last_attendance:
            # print("New last attendance.")
            self.last_attendance = date
        else:
            pass
            # print("Just confused.")
        self.save()
        # print("Final date %s" %(self.last_attendance))


class Teacher(MyModel):
    TEACHER_TYPE = (("TSC", "TSC"), ("BRD", "BOARD"))
    QUALIFICATIONS = (("NS", "Not Set"), ("UNI", "UNIVERSITY"), ("COL", "COLLEGE"))
    first_name = models.CharField(max_length=45)
    middle_name = models.CharField(max_length=45, null=True, blank=True)
    last_name = models.CharField(max_length=45)
    user = models.OneToOneField(MyUser, related_name="teacher", on_delete=models.CASCADE, null=True, blank=True)
    date_started_teaching = models.DateField(null=True, blank=True)
    joined_current_school = models.DateField(null=True, blank=True)
    is_non_delete = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    type = models.CharField(max_length=3, choices=TEACHER_TYPE, default="TSC")
    tsc_no = models.CharField(max_length=45, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True)
    school = models.ForeignKey(School, related_name="teachers", on_delete=models.CASCADE)
    streams = models.ManyToManyField(Stream, null=True, blank=True, related_name="teachers")
    qualifications = models.CharField(max_length=3, choices=QUALIFICATIONS, default="NS", null=True, blank=True)
    is_school_admin = models.BooleanField(default=False)
    email = models.EmailField(max_length=100, null=True, blank=True)
    MARITAL_STATUS = (("NS", "Not Set"), ("S", "Single"), ("M", "Married"), ("D", "Divorced"))
    marital_status = models.CharField(max_length=3, choices=MARITAL_STATUS, default="NS")
    dob = models.DateField(null=True, blank=True)
    moe_id = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return "{} {} {}".format(self.first_name, self.last_name, self.school.name)

    class Meta:
        ordering = ("id",)

    @staticmethod
    def get_role_filters():
        return {"A": None, "SCHA": "school_id", "SCHT": "school_id", "CO": "school__sub_county__county_id", "SCO": "school__sub_county_id",}


TECH_FULL_NAME = Concat(Coalesce("first_name", Value("")), Value(" "), Coalesce("middle_name", Value("")), Value(" "), Coalesce("last_name", Value("")))
TECH_SCHOOL_NAME = F("school__name")
TECH_COUNTY_NAME = F("school__sub_county__county__name")
TECH_SUB_COUNTY_NAME = F("school__sub_county__name")
TEACHER_STATS_DEFINITIONS = {
    "id": {
        "value": F("id"),
        "extra_fields": {
            "full_name": TECH_FULL_NAME,
            "tsc_number": F("tsc_no"),
            "school_name": TECH_SCHOOL_NAME,
            "joined_date": F("joined_current_school"),
            "sub_county_name": TECH_SUB_COUNTY_NAME,
            "username": F("phone"),
            "county_name": TECH_COUNTY_NAME,
        },
        "resp_fields": {"id"},
    },
    "sub-county": {
        "value": F("school__sub_county_id"),
        "extra_fields": {
            "sub_county_name": TECH_SUB_COUNTY_NAME,
            "county_name": TECH_COUNTY_NAME,
        },
    },
    "county": {
        "value": F("school__sub_county_id"),
        "extra_fields": {
            "county_name": TECH_COUNTY_NAME,
        },
    },
}

DEFAULT_TEACHER_FIELDS = {
    "tsc": Count("id", filter=Q(type="TSC")),
    "board": Count("id", filter=Q(type="BRD")),
}


class GraduatesStream(MyModel):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="graduate_streams")
    year = models.PositiveSmallIntegerField(max_length=4)
    name = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        unique_together = ("school", "year")

    def __str__(self):
        return self.school.name + "-" + str(self.year) + "-Graduates"


STUDENT_STATUS = (
    ("OOSC", "Dropped Out"),
    ("NE", "Never Been to School"),
    ("PE", "Already Enrolled"),
)
STUDENT_GENDERS = (("M", "MALE"), ("F", "FEMALE"))


class Student(MyModel):
    TRANSPORT = (("PERSONAL", "Personal Vehicle"), ("BUS", "School Bus"), ("FOOT", "By Foot"), ("NS", "Not Set"))
    TIME_TO_SCHOOL = (("1HR", "One Hour"), ("-0.5HR", "Less than 1/2 Hour"), ("+1HR", "More than one hour."), ("NS", "Not Set"))
    # LIVE_WITH = (('P', 'Parents'), ('G', 'Gurdians'), ('A', 'Alone'), ('NS', 'Not Set'))
    LIVE_WITH = (("B", "Both Parents"), ("S", "Single Parent"), ("N", "None"), ("NS", "Not Set"))

    # admission_no = models.BigIntegerField(null=True, blank=True)
    # school_id     = models.ForeignKey(Schools,on_delete = models.CASCADE)
    emis_code = models.BigIntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_enrolled = models.DateField(default=timezone.now)

    admission_no = models.CharField(max_length=50, null=True, blank=True)
    stream = models.ForeignKey(Stream, null=True, blank=True, on_delete=models.CASCADE, related_name="students")  # shows the current class
    gender = models.CharField(max_length=2, choices=STUDENT_GENDERS, default="M")
    previous_class = models.IntegerField(default=0, null=True, blank=True)
    mode_of_transport = models.CharField(max_length=20, default="NS", choices=TRANSPORT)
    time_to_school = models.CharField(max_length=50, default="NS", choices=TIME_TO_SCHOOL)
    distance_from_school = models.IntegerField(null=True, blank=True)
    household = models.IntegerField(default=0, null=True)  # people in the same house
    meals_per_day = models.IntegerField(default=0, null=True, blank=True)
    not_in_school_before = models.BooleanField(default=False)  # reason for not being in school before
    emis_code_histories = models.CharField(max_length=200, null=True, blank=True)
    total_attendance = models.IntegerField(default=0, null=True, blank=True)
    total_absents = models.IntegerField(default=0, null=True, blank=True)
    last_attendance = models.DateField(null=True, blank=True)
    knows_dob = models.BooleanField(default=True)

    guardian_name = models.CharField(max_length=50, null=True, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True, null=True)
    guardian_status = models.CharField(max_length=20, choices=LIVE_WITH, default="NS")
    guardian_sub_county = models.ForeignKey(SubCounty, null=True, blank=True, on_delete=models.SET_NULL, related_name="students_guardians")
    guardian_email = models.EmailField(null=True, blank=True, max_length=45)

    sub_county = models.ForeignKey(SubCounty, null=True, blank=True, on_delete=models.SET_NULL)
    village = models.CharField(null=True, blank=True, max_length=45)

    cash_transfer_beneficiary = models.BooleanField(default=False)

    active = models.BooleanField(default=True)
    graduated = models.BooleanField(default=False)
    dropout_reason = models.CharField(max_length=200, null=True, blank=True)
    offline_id = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(choices=STUDENT_STATUS, max_length=5, default="NE")
    # special_needs=MultiSelectField(choices=SPECIAL_NEEDS,max_length=10,null=True,blank=True)
    special_needs = models.ManyToManyField(SpecialNeed, null=True, blank=True, related_name="students")
    graduates_class = models.ForeignKey(GraduatesStream, null=True, blank=True, on_delete=models.SET_NULL)
    moe_id = models.CharField(null=True, blank=True, max_length=50)
    moe_unique_id = models.CharField(null=True, blank=True, max_length=45)
    moe_extra_info = models.JSONField(null=True, blank=True)
    upi = models.CharField(max_length=45, null=True, blank=True, help_text="Unique Identification provided by the school")

    # Is it an out of school children
    ##
    class Meta:
        ordering = ("id",)
        indexes = [
            models.Index(fields=["gender"], name="students_gender_indx"),
            models.Index(fields=["id", "gender"], name="students_id_gender_indx"),
        ]

    @staticmethod
    def get_role_filters():
        return {
            "A": None,
            "SCHA": "stream__school_id",
            "SCHT": "stream__school_id",
            "CO": "stream__school__sub_county__county_id",
            "SCO": "stream__school__sub_county_id",
        }

    def __str__(self):
        if self.stream:
            return self.first_name + "(" + self.stream.name + ")"
        return self.first_name

    @property
    def full_name(self):
        return "{} {} {}".format(self.first_name, self.middle_name if self.middle_name != None else "", self.last_name)

    @property
    def age(self):
        if self.date_of_birth:
            # Get today's date object
            today = date.today()

            # A bool that represents if today's day/month precedes the birth day/month
            one_or_zero = (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)

            # Calculate the difference in years from the date object's components
            year_difference = today.year - self.date_of_birth.year

            # The difference in years is not enough.
            # To get it right, subtract 1 or 0 based on if today precedes the
            # birthdate's month/day.

            # To do this, subtract the 'one_or_zero' boolean
            # from 'year_difference'. (This converts
            # True to 1 and False to 0 under the hood.)
            age = year_difference - one_or_zero
            return age

    @property
    def student_id(self):
        if self.admission_no is None and self.upi is None:
            return "XXX / XXX"
        if self.admission_no is None and self.upi is not None:
            return "{} / XXX".format(self.upi)
        if self.admission_no is not None and self.upi is None:
            return "XXX / {}".format(self.admission_no)
        return "{} / {}".format(self.upi, self.admission_no)


STUD_COUNTY_NAME = F("sub_county__county__name")
STUD_SUB_COUNTY_NAME = F("sub_county__name")

STUD_COUNTY_NAME = F("sub_county__county__name")
STUD_SUB_COUNTY_NAME = F("sub_county__name")

SCHOOL_COUNTY_NAME = F("stream__school__sub_county__county__name")
SCHOOL_SUB_COUNTY_NAME = F("stream__school__sub_county__name")

STUD_SCHOOL_NAME = F("stream__school__name")
STUD_SCHOOL_NEMIS_CODE = F("stream__school__emis_code")

STUD_STREAM_NAME = Concat(F("stream__base_class"), Value(" "), Coalesce(F("stream__name"), Value("")))
STUD_FULL_NAME = Concat(Coalesce("first_name", Value("")), Value(" "), Coalesce("middle_name", Value("")), Value(" "), Coalesce("last_name", Value("")))
STUD_FULL_NAMES = Concat(Coalesce("first_name", Value("")), Value(" "), Coalesce("middle_name", Value("")), Value(" "), Coalesce("last_name", Value("")))

STUD_UNIQUE_NAME_CLASS = Concat(
    Coalesce("first_name", Value("X")),
    Value("_"),
    Coalesce("middle_name", Value("X")),
    Value("_"),
    Coalesce("last_name", Value("X")),
    Value("_"),
    Coalesce("upi", Value("X")),
    Value("_"),
    Coalesce("stream_id", Value(0)),
    Value("_"),
    Coalesce("stream__school__emis_code", Value("X")),
    Value("_"),
    Coalesce("date_of_birth", Value("1970-01-01")),
    output_field=CharField(),
)
STUD_PARTNER_NAME = F("stream__school__sub_county__partner_names")


class Month(Func):
    function = "DATE_FORMAT"
    template = "%(function)s(%(expressions)s, '%%b')"
    output_field = CharField()


STUDENTS_STATS_DEFINTIONS = {
    "class": {
        "value": F("stream__base_class"),
        "extra_fields": {
            "class_name": F("stream__base_class"),
        },
    },
    "stream": {
        "value": F("stream_id"),
        "extra_fields": {
            "stream_name": STUD_STREAM_NAME,
            "base_class": F("stream__base_class"),
            "county_name": SCHOOL_COUNTY_NAME,
            "sub_county_name": SCHOOL_SUB_COUNTY_NAME,
            "school_name": STUD_SCHOOL_NAME,
            "school_nemis_code": STUD_SCHOOL_NEMIS_CODE,
            "partner_name": STUD_PARTNER_NAME,
        },
    },
    "school": {
        "value": F("stream__school"),
        "extra_fields": {
            "county_name": SCHOOL_COUNTY_NAME,
            "sub_county_name": SCHOOL_SUB_COUNTY_NAME,
            "school_name": STUD_SCHOOL_NAME,
            "school_nemis_code": STUD_SCHOOL_NEMIS_CODE,
            "partner_name": STUD_PARTNER_NAME,
        },
    },
    "sub-county": {
        "value": F("stream__school__sub_county_id"),
        "extra_fields": {
            "county_name": SCHOOL_COUNTY_NAME,
            "sub_county_name": SCHOOL_SUB_COUNTY_NAME,
            "partner_name": STUD_PARTNER_NAME,
        },
    },
    "partner": {
        "value": STUD_PARTNER_NAME,
        "extra_fields": {
            "partner_name": STUD_PARTNER_NAME,
            # "county_name": SCHOOL_COUNTY_NAME,
            # "sub_county_name": SCHOOL_SUB_COUNTY_NAME,
        },
    },
    "county": {
        "value": F("stream__school__sub_county__county_id"),
        "extra_fields": {
            "county_name": SCHOOL_COUNTY_NAME,
        },
    },
    "duplicate": {
        "value": STUD_UNIQUE_NAME_CLASS,
        "extra_fields": {
            "duplicate_key": F("value"),
            "full_name": STUD_FULL_NAME,
            "school_name": STUD_SCHOOL_NAME,
            "class": STUD_STREAM_NAME,
        },
        "resp_fields": {
            # "count": Count("id"),
        },
        "enabled_filters": {
            "total_students__gt": 1,
        },
    },
    "special-need": {
        "value": F("special_needs__id"),
        "extra_fields": {
            "special_need_name": F("special_needs__name"),
        },
    },
    "gender": {
        "value": F("gender"),
        "extra_fields": {
            "gender_name": case_generator(STUDENT_GENDERS, "gender"),
        },
        "resp_fields": {
            # "count": Count("id"),
        },
    },
    "age": {
        "value": RawSQL("date_part('year',age(date_of_birth))", ()),
        "extra_fields": {
            "age": F("value"),
        },
    },
    "id": {
        "value": F("id"),
        "extra_fields": {
            "full_name": STUD_FULL_NAME,
            "leaner_status": case_generator(STUDENT_STATUS, "status"),
            "leaner_gender": case_generator(STUDENT_GENDERS, "gender"),
            "class": STUD_STREAM_NAME,
            "admission_number": Coalesce(F("admission_no"), Value("XXX")),
            "school_name": STUD_SCHOOL_NAME,
            "school_nemis_code": STUD_SCHOOL_NEMIS_CODE,
            "enrolled_date": F("date_enrolled"),
            "sub_county_name": SCHOOL_SUB_COUNTY_NAME,
            "county_name": SCHOOL_COUNTY_NAME,
            "leaner_in_school": F("active"),
            "partner_name": STUD_PARTNER_NAME,
            #   "special_needs_names": Coalesce(GroupConcat("special_needs__name", delimiter=", "), Value("None")),
        },
        "resp_fields": {
            "id",
            "upi",
            "cash_transfer_beneficiary",
            "date_of_birth",
        },
        "export_only_fields": {
            "special_needs_names": Coalesce(GroupConcat("special_needs__name", delimiter=", "), Value("None")),
        },
    },
    "student-status": {
        "value": F("status"),
        "extra_fields": {
            "status_name": case_generator(STUDENT_STATUS, "status"),
        },
    },
    "dropout-reason": {
        "value": F("dropout_reason"),
    },
    "knows-dob": {
        "value": F("knows_dob"),
    },
    "month": {
        "value": Trunc("date_enrolled", "month", output_field=DateField()),
        "extra_fields": {
            "month": F("value"),
        },
    },
    "year": {
        "value": Trunc("date_enrolled", "year", output_field=DateField()),
        "extra_fields": {
            "year": F("value"),
        },
    },
    "day": {
        "value": TruncDate("date_enrolled", output_field=DateField()),
        "extra_fields": {
            "date": F("value"),
        },
    },
    "week": {
        "value": Trunc("date_enrolled", "week", output_field=DateField()),
        "extra_fields": {
            "week": F("value"),
            # "week_number": ExtractWeek("date"),
        },
    },
}

STUDENTS_STATS_DEFAULT_FIELDS = {
    "males": Count("id", filter=Q(gender="M")),
    "females": Count("id", filter=Q(gender="F")),
}


class DeleteReason(MyModel):
    name = models.CharField(unique=True, max_length=45)
    description = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("id",)


class StudentDeleteReason(MyModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reason = models.ForeignKey(DeleteReason, on_delete=models.CASCADE)
    description = models.TextField(max_length=1500, null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.student.first_name, self.reason.name)

    class Meta:
        ordering = ("id",)

    @staticmethod
    def get_role_filters():
        return {
            "A": None,
            "SCHA": "student__stream__school_id",
            "SCHT": "student__stream__school_id",
            "CO": "student__stream__school__sub_county__county_id",
            "SCO": "student__stream__school__sub_county_id",
        }


REASON_DESCRIPTION = Case(
    When(
        reason__name="other",
        then=F("description"),
    ),
    default=F("reason__description"),
    output_field=CharField(),
)

STUD_SCHOOL_NAME = F("student__stream__school__name")
STUD_STATUS = case_generator(STUDENT_STATUS, "student__status")
STUD_STREAM_NAME = Concat(F("student__stream__base_class"), Value(" "), Coalesce(F("student__stream__name"), Value("")))
STUD_FULL_NAME = Concat(Coalesce("student__first_name", Value("")), Value(" "), Coalesce("student__middle_name", Value("")), Value(" "), Coalesce("student__last_name", Value("")))

STUDENT_DELETE_REASON_STATS_DEFINTIONS = {
    "id": {
        "value": F("id"),
        "extra_fields": {
            "date_added": TruncDay("created", output_field=DateField()),
            "full_name": STUD_FULL_NAME,
            "gender": case_generator(STUDENT_GENDERS, "student__gender"),
            "admission_number": Coalesce(F("student__admission_no"), Value("XXX")),
            "class": STUD_STREAM_NAME,
            "school_name": STUD_SCHOOL_NAME,
            "sub_county_name": F("student__stream__school__sub_county__name"),
            "county_name": F("student__stream__school__sub_county__county__name"),
            "date_of_birth": F("student__date_of_birth"),
            "date_enrolled": F("student__date_enrolled"),
            "student_status": STUD_STATUS,
            "reason_name": F("reason__description"),
            "cash_transfer_beneficiary": F("student__cash_transfer_beneficiary"),
            "admission_number": Coalesce(F("student__admission_no"), Value("XXX")),
            "upi": Coalesce(F("student__upi"), Value("XXX")),
            "other_reason": Case(When(description__isnull=False, then=F("description")), default=Value("")),  # F("description"),
            # "leaner_in_school": F("student__active"),
        },
        "resp_fields": {
            # "description",
        },
        "export_only_fields": {
            "special_needs_names": Coalesce(GroupConcat("student__special_needs__name", delimiter=", "), Value("None")),
        },
    },
    "class": {
        "value": F("student__stream__base_class"),
        "extra_fields": {
            "class_name": F("student__stream__base_class"),
        },
    },
    "gender": {
        "value": F("student__gender"),
        "extra_fields": {},
        "resp_fields": {},
    },
    "reason": {
        "value": F("reason_id"),
        "extra_fields": {
            "reason_name": F("reason__description"),
        },
    },
    "reason-description": {
        "value": REASON_DESCRIPTION,
        "extra_fields": {},
        # "resp_fields": {},
    },
}
STUDENT_DELETE_REASON_STATS_DEFAULT_RESP_FIELDS = {
    "males": Count("id", filter=Q(student__gender="M")),
    "females": Count("id", filter=Q(student__gender="F")),
}


class AbsentReason(MyModel):
    name = models.CharField(unique=True, max_length=45)
    description = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("id",)


class StudentAbsentReason(MyModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reason = models.ForeignKey(AbsentReason, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField(max_length=1500, null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.student.first_name, self.reason.name)

    class Meta:
        ordering = ("id",)
        unique_together = ("student", "date")

    @staticmethod
    def get_role_filters():
        return {
            "A": None,
            "SCHA": "student__stream__school_id",
            "SCHT": "student__stream__school_id",
            "CO": "student__stream__school__sub_county__county_id",
            "SCO": "student__stream__school__sub_county_id",
        }


STUDENT_ABSENT_REASON_STATS_DEFINTIONS = {
    "id": {
        "value": F("id"),
        "extra_fields": {
            "date_added": TruncDay("created", output_field=DateField()),
            "full_name": STUD_FULL_NAME,
            "gender": case_generator(STUDENT_GENDERS, "student__gender"),
            "admission_number": Coalesce(F("student__admission_no"), Value("XXX")),
            "class": STUD_STREAM_NAME,
            "school_name": STUD_SCHOOL_NAME,
            "sub_county_name": F("student__stream__school__sub_county__name"),
            "county_name": F("student__stream__school__sub_county__county__name"),
            "date_of_birth": F("student__date_of_birth"),
            "date_enrolled": F("student__date_enrolled"),
            "student_status": STUD_STATUS,
            "reason_name": F("reason__description"),
            "cash_transfer_beneficiary": F("student__cash_transfer_beneficiary"),
            "admission_number": Coalesce(F("student__admission_no"), Value("XXX")),
            "upi": Coalesce(F("student__upi"), Value("XXX")),
            "other_reason": Case(When(description__isnull=False, then=F("description")), default=Value("")),  # F("description"),
            # "leaner_in_school": F("student__active"),
        },
        "resp_fields": {
            # "description",
        },
        "export_only_fields": {
            "special_needs_names": Coalesce(GroupConcat("student__special_needs__name", delimiter=", "), Value("None")),
        },
    },
    "class": {
        "value": F("student__stream__base_class"),
        "extra_fields": {
            "class_name": F("student__stream__base_class"),
        },
    },
    "gender": {
        "value": F("student__gender"),
        "extra_fields": {},
        "resp_fields": {},
    },
    "reason": {
        "value": F("reason_id"),
        "extra_fields": {
            "reason_name": F("reason__description"),
        },
    },
    "reason-description": {
        "value": REASON_DESCRIPTION,
        "extra_fields": {},
        # "resp_fields": {},
    },
}
STUDENT_ABSENT_REASON_STATS_DEFAULT_RESP_FIELDS = {
    "males": Count("id", filter=Q(student__gender="M")),
    "females": Count("id", filter=Q(student__gender="F")),
}


IMPORT_STEPS = (
    ("Q", "Queued"),
    ("VH", "Validating Required Columns..."),
    ("PI", "Preparing..."),
    ("I", "Processing..."),
    ("F", "Failed"),
    ("D", "Done"),
)


IMPORT_TYPES = (
    ("F", "Import File"),
    ("NMC", "Nemis County"),
    ("NMSC", "Nemis Sub County"),
    ("NMSCH", "Nemis School"),
    ("JS", "Json Data"),
)


class SchoolsStudentsImport(MyModel):
    name = models.CharField(max_length=45, null=True, blank=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    import_file = models.FileField(upload_to="imports", null=True, blank=True)
    import_type = models.CharField(max_length=5, choices=IMPORT_TYPES, default="F")
    step = models.CharField(choices=IMPORT_STEPS, default="Q", max_length=3, editable=False)
    errors_file = models.FileField(upload_to="imports", null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True, editable=False)
    end_time = models.DateTimeField(null=True, blank=True, editable=False)
    args = models.TextField(max_length=1000, null=True, blank=True, editable=False)
    rows_count = models.IntegerField(default=0, editable=False)
    imported_rows_count = models.IntegerField(default=0, editable=False)
    duplicates_count = models.IntegerField(default=0, editable=False)
    error_rows_count = models.IntegerField(default=0, editable=False)
    new_students_created = models.IntegerField(default=0, editable=False)
    should_import = models.BooleanField(default=True)
    nemis_group_id = models.CharField(max_length=45, help_text="The County Id, Sub county Id, School Id", null=True, blank=True)
    nemis_institution_level = models.CharField(max_length=45, help_text="Nemis Institution Level", null=True, blank=True)
    raw_data = models.JSONField(null=True, blank=True)
    errors = models.TextField(max_length=2000, default="")
    update_learner = models.BooleanField(default=False)

    class Meta:
        ordering = ("-id",)

    @property
    def is_clean(self):
        if self.step != "D":
            return False
        if self.errors:
            return False
        return self.error_rows_count == 0

    @property
    def completed_steps(self):
        return []

    @property
    def duration(self):
        if self.start_time is None or self.end_time is None:
            return 0
        return self.end_time - self.start_time

    def prepare_import(self):
        self.imported_rows_count = 0
        self.rows_count = 0
        self.duplicates_count = 0
        self.step = "VH"
        self.errors = ""
        self.start_time = timezone.now()
        self.save()

    def start(self, rows_count):
        self.rows_count = rows_count
        self.step = "I"
        self.save()

    def append_count(self, rows_count):
        self.imported_rows_count += rows_count
        self.save()

    def finish(self, errors_file_path="", status="D", error_rows_count=0):
        if errors_file_path != "":
            self.errors_file.name = errors_file_path
        self.step = status
        self.end_time = timezone.now()
        self.error_rows_count += error_rows_count
        self.save()

    def set_errors(self, errors):
        self.errors = ""
        self.errors = errors
        self.step = "F"
        self.save()
