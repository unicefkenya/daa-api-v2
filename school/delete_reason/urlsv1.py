from django.conf.urls import url

from school.delete_reason.views import ListCreateDeleteReasonsAPIView, ListStudentDeleteReasonDynamicStatisticsAPIView, RetrieveUpdateDestroyDeleteReasonAPIView

urlpatterns = [
    url(r"^$", ListCreateDeleteReasonsAPIView.as_view(), name="list_create_delete_reasons"),
    url(r"^(?P<pk>[0-9]+)/?$", RetrieveUpdateDestroyDeleteReasonAPIView.as_view(), name="retrieve_update_destroy_delete_reason"),
    url(r"^stats/(?P<type>.+)/?$", ListStudentDeleteReasonDynamicStatisticsAPIView.as_view(), name="list_dynamic_student_delete_reasonss_statistics"),
]
