from django.conf.urls import url, include

from attendance.views import (
    GetStatsAttendanceAPIView,
    ListAttendanceDynamicStatisticsAPIView,
    ListCreateAttendancesAPIView,
    RetrieveUpdateDestroyAttendanceAPIView,
    ListCreateAttendanceStatistics,
    ListCreateStreamAttendance,
)

urlpatterns = [
    url(r"^student-absent-reasons/", include("attendance.student_absent_reason.urlsv1")),
    url(r"^$", ListCreateStreamAttendance.as_view(), name="list_create_attendances"),
    url(r"^(?P<pk>[0-9]+)/?$", RetrieveUpdateDestroyAttendanceAPIView.as_view(), name="retrieve_update_destroy_attendance"),
    url(r"^stats/(?P<type>.+)/?$", ListAttendanceDynamicStatisticsAPIView.as_view(), name="list_dynamic_attendances_statistics"),
    url(r"^stats/?$", GetStatsAttendanceAPIView.as_view(), name="list_dynamic_attendances_statistics"),
    url(r"^(?P<type>.+)/?$", ListCreateAttendanceStatistics.as_view(), name="list_create_attendance_statistics"),
    # url(r'^(?P<pk>[0-9]+)/districts/?$', ListAttendanceDistricts.as_view(), name="list_attendance_districts"),
]
