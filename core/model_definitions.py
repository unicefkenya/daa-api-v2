from attendance.filters import AttendanceFilter
from school.models import (
    STUDENT_DELETE_REASON_STATS_DEFAULT_RESP_FIELDS,
    STUDENT_DELETE_REASON_STATS_DEFINTIONS,
    Student,
    STUDENTS_STATS_DEFINTIONS,
    STUDENTS_STATS_DEFAULT_FIELDS,
    TEACHER_STATS_DEFINITIONS,
    DEFAULT_TEACHER_FIELDS,
    DEFAULT_SCHOOL_FIELDS,
    SCHOOL_STATS_DEFINITIONS,
)
from attendance.models import ATTENDANCE_STATS_DEFAULT_FIELDS, ATTENDANCE_STATS_DEFINTIONS

# ATTENDANCE_TRACKING_STATS_DEFAULT_FIELDS, ATTENDANCE_TRACKING_STATS_DEFINTIONS

from school.student.filters import EnrollmentFilter
from school.student.serializers import StudentSerializer

training_school_default = False
models_definitions = {
    "Student": {
        "stats_definition": STUDENTS_STATS_DEFINTIONS,
        "default_fields": STUDENTS_STATS_DEFAULT_FIELDS,
        "filter_mixin": EnrollmentFilter,
        "default_filters": {
            "is_training_school": {
                "field_name": "stream__school__is_training_school",
                "value": training_school_default,
            },
        },
    },
    "Attendance": {
        "stats_definition": ATTENDANCE_STATS_DEFINTIONS,
        "default_fields": ATTENDANCE_STATS_DEFAULT_FIELDS,
         "filter_mixin":AttendanceFilter,
        "default_filters": {
            "is_training_school": {
                "field_name": "stream__school__is_training_school",
                "value": training_school_default,
            },
        },
    },
    "Teacher": {
        "stats_definition": TEACHER_STATS_DEFINITIONS,
        "default_fields": DEFAULT_TEACHER_FIELDS,
        "default_filters": {
            "is_training_school": {
                "field_name": "school__is_training_school",
                "value": training_school_default,
            },
        },
    },
    "School": {
        "stats_definition": SCHOOL_STATS_DEFINITIONS,
        "default_fields": DEFAULT_SCHOOL_FIELDS,
        "default_filters": {
            "is_training_school": {
                "field_name": "is_training_school",
                "value": training_school_default,
            },
        },
    },
    "StudentDeleteReason": {
        "stats_definition": STUDENT_DELETE_REASON_STATS_DEFINTIONS,
        "default_fields": STUDENT_DELETE_REASON_STATS_DEFAULT_RESP_FIELDS,
        "default_filters": {
            "is_training_school": {
                "field_name": "student__stream__school__is_training_school",
                "value": training_school_default,
            },
        },
    },
    "StudentAbsentReason": {
        "stats_definition": STUDENT_DELETE_REASON_STATS_DEFINTIONS,
        "default_fields": STUDENT_DELETE_REASON_STATS_DEFAULT_RESP_FIELDS,
        "default_filters": {
            "is_training_school": {
                "field_name": "student__stream__school__is_training_school",
                "value": training_school_default,
            },
        },
    },
    # "NoAttendanceHistory": {
    #     "stats_definition": ATTENDANCE_TRACKING_STATS_DEFINTIONS,
    #     "default_fields": ATTENDANCE_TRACKING_STATS_DEFAULT_FIELDS,
    # },
}
