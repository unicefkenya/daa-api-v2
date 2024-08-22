import django_filters

from school.models import School
from django_filters.rest_framework import FilterSet


class SchoolFilter(FilterSet):
    county = django_filters.NumberFilter(field_name="sub_county__county_id", label="School Sub County Id")

    # field_name = "stream__school__sub_county__county_id"
    class Meta:
        model = School
        fields = "__all__"


BASE_STUDENT_REASON_FILTERS = [
    {"field_name": "student__stream__school_id", "label": "School Id", "field_type": "number"},
    {"field_name": "student__stream__base_class", "label": "Base Class", "field_type": "char"},
    {"field_name": "created__date", "label": "Recorded Date", "field_type": "date"},
    {
        "field_name": "created__date",
        "lookup_expr": "gte",
        "label": "Start Recorded Date",
        "field_type": "date",
    },
    {
        "field_name": "created__date",
        "lookup_expr": "lte",
        "label": "End Recorded Date",
        "field_type": "date",
    },
    {"field_name": "student__stream_id", "label": "Stream Id", "field_type": "number"},
    {"field_name": "student__stream__school__sub_county_id", "label": "Sub County Id", "field_type": "number"},
    {"field_name": "student__stream__school__sub_county__county_id", "label": "County Id", "field_type": "number"},
]
