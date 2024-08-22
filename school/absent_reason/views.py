from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from attendance.student_absent_reason.serializers import StudentAbsentReasonSerializer
from school.filters import BASE_STUDENT_REASON_FILTERS

from school.models import STUDENT_DELETE_REASON_STATS_DEFAULT_RESP_FIELDS, STUDENT_DELETE_REASON_STATS_DEFINTIONS, AbsentReason, StudentAbsentReason
from school.absent_reason.serializers import AbsentReasonSerializer
from mylib.my_common import MyDjangoFilterBackend, MyStandardPagination, FilterBasedOnRole
from drf_autodocs.decorators import format_docstring

from stats.views import MyCustomDyamicStats


class ListCreateAbsentReasonsAPIView(FilterBasedOnRole, generics.ListCreateAPIView):
    serializer_class = AbsentReasonSerializer
    queryset = AbsentReason.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    pagination_class = MyStandardPagination

    def perform_create(self, serializer):
        serializer.save()


class RetrieveUpdateDestroyAbsentReasonAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AbsentReasonSerializer
    queryset = AbsentReason.objects.all()


ABSENT_REASON_EXTRA_FILTERS = [
    *BASE_STUDENT_REASON_FILTERS,
    {
        "field_name": "date",
        "lookup_expr": "gte",
        "label": "Start Attendance Date",
        "field_type": "date",
    },
    {
        "field_name": "date",
        "lookup_expr": "lte",
        "label": "End Attendance Date",
        "field_type": "date",
    },
]

STUDENT_ABSENT_REASON_SUPPOERTED_STAT_TYES = [stat for stat in STUDENT_DELETE_REASON_STATS_DEFINTIONS]
STUDENT_ABSENT_REASON_STATS_DEFINTIONS = STUDENT_DELETE_REASON_STATS_DEFINTIONS
STUDENT_ABSENT_REASON_STATS_DEFAULT_RESP_FIELDS = STUDENT_DELETE_REASON_STATS_DEFAULT_RESP_FIELDS


@format_docstring({}, stat_types=", ".join(STUDENT_ABSENT_REASON_SUPPOERTED_STAT_TYES))
class ListStudenAbsentReasonDynamicStatisticsAPIView(MyCustomDyamicStats, generics.ListAPIView):
    """
    Group statistics by:
    `type` = {stat_types}
    """

    # serializer_class = StudentAbsentReasonSerializer
    queryset = StudentAbsentReason.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    stat_type = ""
    # filter_mixin=AttendanceFilter
    count_name = "total_absent_reasons"
    stats_definitions = STUDENT_ABSENT_REASON_STATS_DEFINTIONS
    default_fields = STUDENT_ABSENT_REASON_STATS_DEFAULT_RESP_FIELDS
    extra_filter_fields = ABSENT_REASON_EXTRA_FILTERS
