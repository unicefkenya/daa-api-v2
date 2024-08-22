from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from school.filters import BASE_STUDENT_REASON_FILTERS

from school.models import STUDENT_DELETE_REASON_STATS_DEFAULT_RESP_FIELDS, STUDENT_DELETE_REASON_STATS_DEFINTIONS, DeleteReason, StudentDeleteReason
from school.delete_reason.serializers import DeleteReasonSerializer
from mylib.my_common import MyDjangoFilterBackend, MyStandardPagination, FilterBasedOnRole
from drf_autodocs.decorators import format_docstring

from school.student.serializers import DeleteStudentSerializer
from stats.views import MyCustomDyamicStats


class ListCreateDeleteReasonsAPIView(FilterBasedOnRole, generics.ListCreateAPIView):
    serializer_class = DeleteReasonSerializer
    queryset = DeleteReason.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    pagination_class = MyStandardPagination

    def perform_create(self, serializer):
        serializer.save()


class RetrieveUpdateDestroyDeleteReasonAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeleteReasonSerializer
    queryset = DeleteReason.objects.all()
    permission_classes = (IsAuthenticated,)


STUDENT_DELETE_REASON_SUPPOERTED_STAT_TYES = [stat for stat in STUDENT_DELETE_REASON_STATS_DEFINTIONS]


@format_docstring({}, stat_types=", ".join(STUDENT_DELETE_REASON_SUPPOERTED_STAT_TYES))
class ListStudentDeleteReasonDynamicStatisticsAPIView(MyCustomDyamicStats, generics.ListAPIView):
    """
    Group statistics by:
    `type` = {stat_types}
    """

    serializer_class = DeleteStudentSerializer
    queryset = StudentDeleteReason.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    stat_type = ""
    # filter_mixin=AttendanceFilter
    count_name = "total_deactivations"
    stats_definitions = STUDENT_DELETE_REASON_STATS_DEFINTIONS
    default_fields = STUDENT_DELETE_REASON_STATS_DEFAULT_RESP_FIELDS
    extra_filter_fields = BASE_STUDENT_REASON_FILTERS
