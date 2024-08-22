from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from school.filters import BASE_STUDENT_REASON_FILTERS

from school.models import StudentAbsentReason
from attendance.student_absent_reason.serializers import StudentAbsentReasonSerializer
from mylib.my_common import MyDjangoFilterBackend, MyStandardPagination


class ListCreateStudentAbsentReasonsAPIView(generics.ListCreateAPIView):
    serializer_class = StudentAbsentReasonSerializer
    queryset = StudentAbsentReason.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    pagination_class = MyStandardPagination
    extra_filter_fields = BASE_STUDENT_REASON_FILTERS

    def perform_create(self, serializer):
        serializer.save()


class RetrieveUpdateDestroyStudentAbsentReasonAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentAbsentReasonSerializer
    queryset = StudentAbsentReason.objects.all()
