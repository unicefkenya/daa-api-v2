from django.conf.urls import url

from school.absent_reason.views import ListCreateAbsentReasonsAPIView, ListStudenAbsentReasonDynamicStatisticsAPIView, RetrieveUpdateDestroyAbsentReasonAPIView

urlpatterns = [
    url(r"^$", ListCreateAbsentReasonsAPIView.as_view(), name="list_create_absent_reasons"),
    url(r"^(?P<pk>[0-9]+)/?$", RetrieveUpdateDestroyAbsentReasonAPIView.as_view(), name="retrieve_update_destroy_absent_reason"),
    url(r"^stats/(?P<type>.+)/?$", ListStudenAbsentReasonDynamicStatisticsAPIView.as_view(), name="list_dynamic_student_absent_reasons_statistics"),
]
