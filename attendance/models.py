from django.db import models

# Create your models here.
from django.db.models import Count, Q, F, DateField, Value, FloatField, DecimalField, IntegerField
from django.db.models.expressions import RawSQL, Func
from django.db.models.functions import Trunc, TruncDate, ExtractYear, Concat, Coalesce, Cast

from mylib.my_common import MyModel, case_generator
from mylib.mygenerics import GroupConcat
from school.models import STUDENT_GENDERS, STUDENT_STATUS, Student, Stream, Teacher

ATTENDANCE_STATUS = ((1, "Present"), (0, "Absent"))


class Attendance(models.Model):
    id = models.CharField(primary_key=True, max_length=70)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateTimeField()
    status = models.IntegerField(choices=ATTENDANCE_STATUS, default=0)  # assuming 1 is present 0 is absent
    cause_of_absence = models.CharField(max_length=200, null=True, blank=True)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student)

    class Meta:
        ordering = ("id",)
        # unique_together=
        get_latest_by = "date"

    @staticmethod
    def get_role_filters():
        return {
            "A": None,
            "SCHA": "stream__school_id",
            "SCHT": "stream__school_id",
            "CO": "stream__school__sub_county__county_id",
            "SCO": "stream__school__sub_county_id",
        }


STUD_COUNTY_NAME = F("sub_county__county__name")
STUD_SUB_COUNTY_NAME = F("sub_county__name")
STUD_SCHOOL_NAME = F("stream__school__name")
STUD_SCHOOL_NEMIS_CODE = F("stream__school__emis_code")
STUD_STATUS = case_generator(STUDENT_STATUS, "student__status")
STUD_STREAM_NAME = Concat(F("stream__base_class"), Value(" "), Coalesce(F("stream__name"), Value("")))
STUD_FULL_NAME = Concat(Coalesce("student__first_name", Value("")), Value(" "), Coalesce("student__middle_name", Value("")), Value(" "), Coalesce("student__last_name", Value("")))


ATT_COUNTY_NAME = F("stream__school__sub_county__county__name")
ATT_SUB_COUNTY_NAME = F("stream__school__sub_county__name")
ATT_PARTNER_NAME = F("stream__school__sub_county__partner_names")

ATTENDANCE_STATS_DEFINTIONS = {
    "id": {
        "value": F("id"),
        "extra_fields": {
            # "attendance_id":F("id"),
            "attendance": case_generator(ATTENDANCE_STATUS, "status"),
            "attendance_date": TruncDate("date", output_field=DateField()),
            "full_name": STUD_FULL_NAME,
            "gender": case_generator(STUDENT_GENDERS, "student__gender"),
            "admission_number": Coalesce(F("student__admission_no"), Value("XXX")),
            "class": STUD_STREAM_NAME,
            "school_name": STUD_SCHOOL_NAME,
            "school_nemis_code": STUD_SCHOOL_NEMIS_CODE,
            "sub_county_name": ATT_SUB_COUNTY_NAME,
            "county_name": ATT_COUNTY_NAME,
            "student_status": STUD_STATUS,
            "date_of_birth": F("student__date_of_birth"),
            "date_enrolled": F("student__date_enrolled"),
            "leaner_in_school": F("student__active"),
            "partner_name": ATT_PARTNER_NAME,
            "cash_transfer_beneficiary": F("student__cash_transfer_beneficiary"),
            "admission_number": Coalesce(F("student__admission_no"), Value("XXX")),
            "upi": Coalesce(F("student__upi"), Value("XXX")),
        },
        "resp_fields": {
            "id"
            # "id": F("id"),
            # "status": F("status")
        },
        "export_only_fields": {
            "special_needs_names": Coalesce(GroupConcat("student__special_needs__name", delimiter=", "), Value("None")),
        },
    },
    "student": {
        "value": F("student_id"),
        "extra_fields": {
            "full_name": STUD_FULL_NAME,
            "gender": case_generator(STUDENT_GENDERS, "student__gender"),
            "admission_number": Coalesce(F("student__admission_no"), Value("XXX")),
            "class": STUD_STREAM_NAME,
            "school_name": STUD_SCHOOL_NAME,
            "school_nemis_code": STUD_SCHOOL_NEMIS_CODE,
            "sub_county_name": F("stream__school__sub_county__name"),
            "county_name": F("stream__school__sub_county__county__name"),
            "student_status": STUD_STATUS,
            "leaner_in_school": F("student__active"),
            "date_of_birth": F("student__date_of_birth"),
            "partner_name": ATT_PARTNER_NAME,
            "date_enrolled": F("student__date_enrolled"),
            "cash_transfer_beneficiary": F("student__cash_transfer_beneficiary"),
            "admission_number": Coalesce(F("student__admission_no"), Value("XXX")),
            "upi": Coalesce(F("student__upi"), Value("XXX")),
        },
        "resp_fields": {
            "present_count": Count("id", filter=Q(status=1)),
            "absent_count": Count("id", filter=Q(status=0)),
        },
        "export_only_fields": {
            "special_needs_names": Coalesce(GroupConcat("student__special_needs__name", delimiter=", "), Value("None")),
        },
    },
    "stream": {
        "value": F("stream_id"),
        "extra_fields": {
            "stream_name": STUD_STREAM_NAME,
            "base_class": F("stream__base_class"),
            "sub_county_name": ATT_SUB_COUNTY_NAME,
            "county_name": ATT_COUNTY_NAME,
            "school_name": F("stream__school__name"),
            "school_nemis_code": STUD_SCHOOL_NEMIS_CODE,
        },
    },
    "class": {
        "value": F("stream__base_class"),
        "extra_fields": {
            "class_name": F("stream__base_class"),
        },
    },
    "school": {
        "value": F("stream__school_id"),
        "extra_fields": {
            "sub_county_name": ATT_SUB_COUNTY_NAME,
            "county_name": ATT_COUNTY_NAME,
            "school_name": F("stream__school__name"),
            "school_nemis_code": STUD_SCHOOL_NEMIS_CODE,
            "partner_name": ATT_PARTNER_NAME,
        },
    },
    "sub-county": {
        "value": F("stream__school__sub_county_id"),
        "extra_fields": {
            "sub_county_name": F("stream__school__sub_county__name"),
            "county_name": F("stream__school__sub_county__county__name"),
            "partner_name": ATT_PARTNER_NAME,
        },
    },
    "partner": {
        "value": ATT_PARTNER_NAME,
        "extra_fields": {
            "partner_name": ATT_PARTNER_NAME,
            # "county_name": SCHOOL_COUNTY_NAME,
            # "sub_county_name": SCHOOL_SUB_COUNTY_NAME,
        },
    },
    "county": {
        "value": F("stream__school__sub_county__county_id"),
        "extra_fields": {
            "county_name": F("stream__school__sub_county__county__name"),
        },
    },
    "special-need": {
        "value": F("student__special_needs__id"),
        "extra_fields": {
            "special_need_name": F("student__special_needs__name"),
        },
    },
    "age": {
        "value": RawSQL(
            """
        date_part('year',age("school_student"."date_of_birth"))::int
        """,
            (),
        ),
        "extra_fields": {
            "age": F("value"),
        },
    },
    "gender": {
        "value": F("student__gender"),
        "extra_fields": {
            "gender_name": case_generator(STUDENT_GENDERS, "value"),
        },
        "resp_fields": {
            "present_count": Count("id", filter=Q(status=1)),
            "absent_count": Count("id", filter=Q(status=0)),
        },
    },
    "student-status": {
        "value": F("student__status"),
        "extra_fields": {
            "status_name": STUD_STATUS,
        },
    },
    "dropout-reason": {
        "value": F("student__dropout_reason"),
    },
    "knows-dob": {
        "value": F("student__knows_dob"),
    },
    "month": {
        "value": Trunc("date", "month", output_field=DateField()),
        "extra_fields": {
            "month": F("value"),
        },
    },
    "year": {
        "value": Trunc("date", "year", output_field=DateField()),
        "extra_fields": {
            "year": F("value"),
        },
    },
    "day": {
        "value": TruncDate("date", output_field=DateField()),
        "extra_fields": {
            "day": F("value"),
        },
    },
    "week": {
        "value": Trunc("date", "week", output_field=DateField()),
        "extra_fields": {
            "week": F("value"),
            # "week_number": ExtractWeek("date"),
        },
    },
}

PRESENT_MALES = Count("id", filter=Q(status=1, student__gender="M"))
ABSENT_MALES = Count("id", filter=Q(status=0, student__gender="M"))
TOTAL_MALES = Count("id", filter=Q(student__gender="M"))


PRESENT_FEMALES = Count("id", filter=Q(status=1, student__gender="F"))
ABSENT_FEMALES = Count("id", filter=Q(status=0, student__gender="F"))
TOTAL_FEMALES = Count("id", filter=Q(student__gender="F"))


# =Cast(Count('name') / 2.0, FloatField()))
class Round(Func):
    function = "ROUND"
    arity = 2


RESP_FLOAT_FIELD = DecimalField(decimal_places=2)

ATTENDANCE_STATS_DEFAULT_FIELDS = {
    "present_males": PRESENT_MALES,
    # "present_males_percentage": Round(PRESENT_MALES * Value(100.0) /  TOTAL_MALES ,1,output_field=FloatField()),
    "absent_males": ABSENT_MALES,
    # "absent_males_percentage":Round( ABSENT_MALES * Value(100.0) /  TOTAL_MALES ,1,output_field=FloatField()),
    "present_females": PRESENT_FEMALES,
    # "present_females_percentage":Round( PRESENT_FEMALES * Value(100.0)  /  TOTAL_FEMALES,1,output_field=FloatField()),
    "absent_females": ABSENT_FEMALES,
    # "absent_females_percentage":Round( ABSENT_FEMALES * Value(100.0) / TOTAL_FEMALES,1,output_field=FloatField()),
}

# total*1.0/SUM(total)
ATTENDANCE_STATS_DEFAULT_FIELDS_PERCENTAGE = {
    "present_males_percentage": Round(PRESENT_MALES * Value(100.0) / Count("id"), 1, output_field=FloatField()),
    "absent_males_percentage": Round(ABSENT_MALES * Value(100.0) / Count("id"), 1, output_field=FloatField()),
    "present_females_percentage": Round(PRESENT_FEMALES * Value(100.0) / Count("id"), 1, output_field=FloatField()),
    "absent_females_percentage": Round(ABSENT_FEMALES * Value(100.0) / Count("id"), 1, output_field=FloatField()),
}


class AttendanceHistory(models.Model):
    date = models.DateField()
    id = models.CharField(primary_key=True, blank=True, max_length=50)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    present = models.IntegerField(default=0)
    absent = models.IntegerField(default=0)


class TeacherAttendance(MyModel):
    ATTENDANCE = ((1, "Present"), (0, "Absent"))
    id = models.CharField(primary_key=True, max_length=70)
    date = models.DateField()
    status = models.IntegerField(choices=ATTENDANCE, default=0)  # assuming 1 is present 0 is absent
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
