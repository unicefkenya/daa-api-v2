from django.db.models import Value, F, DateField, Count, Sum, Min, Max, Q
from django.db.models.functions import Concat, Trunc, TruncDate, Coalesce
from drf_autodocs.decorators import format_docstring
from rest_framework.permissions import IsAuthenticated

from attendance.models import TeacherAttendance
from attendance.v2.serializers import BaseTeacherAttendanceDynamicStatsSerializer
from mylib.my_common import MyDjangoFilterBackend

from rest_framework import generics

from stats.views import MyCustomDyamicStats


REPAIRS_STATS_DEFINTIONS = {
    # "technician": {
    #     "value": F("technician_id"),
    #     "extra_fields": {
    #         "full_name": Concat(F("technician__first_name"), Value(" "), F("technician__first_name")),
    #     }
    # },
    # "insurance": {
    #     "value": F("insurance_id"),
    #     "extra_fields": {
    #         "name": F("insurance__name"),
    #     }
    # },
    "monthly": {"value": Trunc("date", "month", output_field=DateField())},
    "daily": {"value": TruncDate("date", output_field=DateField())},
}

SUPPOERTED_STAT_TYES = [stat for stat in REPAIRS_STATS_DEFINTIONS]


@format_docstring({}, stat_types=", ".join(SUPPOERTED_STAT_TYES))
class TeacherAttendanceStatsAPIView(MyCustomDyamicStats, generics.ListAPIView):
    """
    Group statistics by:
    `type` = {stat_types}
    """

    serializer_class = BaseTeacherAttendanceDynamicStatsSerializer
    queryset = TeacherAttendance.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    SUPPOERTED_STAT_TYES = SUPPOERTED_STAT_TYES
    stat_type = ""
    count_name = "attendances"
    stats_definitions = REPAIRS_STATS_DEFINTIONS

    def get_fields(self):
        return {
            self.count_name: Count("id", distinct=True),
            "present": Count("id", distinct=True, filter=Q(status=1)),
            "absent": Count("id", distinct=True, filter=Q(status=0)),
        }

    def get_serializer_class(self):
        return self.serializer_class

    def get_order_by_default_field(self):
        return self.count_name
