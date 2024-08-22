from django.conf.urls import url

from attendance.v2.views import TeacherAttendanceStatsAPIView

urlpatterns= [
    url(r'^stats/(?P<type>.+)/?$', TeacherAttendanceStatsAPIView.as_view(),
        name="list_dynamic_teacher_attendance_statistics"),
]