from django.conf.urls import url

from school.student.views import (
    GetStatsStudentsAPIView,
    ListCreateStudentsAPIView,
    RetrieveUpdateDestroyStudentAPIView,
    ListCreateBulkStudents,
    GetStudentsEnrollment,
    ListAbsentStudentsAPIView,
    ListDropoutStudents,
    ListStudentsDynamicsAPIView,
)

urlpatterns = [
    url(r"^$", ListCreateStudentsAPIView.as_view(), name="list_create_students"),
    url(r"^dropouts/?$", ListDropoutStudents.as_view(), name="list_dropout_students"),
    url(r"^bulk/?$", ListCreateBulkStudents.as_view(), name="list_create_bulk_students"),
    url(r"^absents/?$", ListAbsentStudentsAPIView.as_view(), name="list_absent_students"),
    url(r"^(?P<pk>[0-9]+)/?$", RetrieveUpdateDestroyStudentAPIView.as_view(), name="retrieve_update_destroy_student"),
    url(r"^stats/(?P<type>.+)", ListStudentsDynamicsAPIView.as_view(), name="list_dynamic_students_statistics"),
    url(r"^stats/", GetStatsStudentsAPIView.as_view(), name="list_dynamic_students_stats_stats"),
    url(r"^enrolls/(?P<type>.+)", ListStudentsDynamicsAPIView.as_view(), name="list_students_enrollments"),
]
