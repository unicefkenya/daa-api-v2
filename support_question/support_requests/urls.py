
from django.conf.urls import url
from support_question.support_requests.views import ListCreateSupportRequestsAPIView, RetrieveUpdateDestroySupportRequestAPIView
urlpatterns=[
    url(r'^$',ListCreateSupportRequestsAPIView.as_view(),name="list_create_support_requests"),
    url(r'^(?P<pk>[0-9]+)/?$',RetrieveUpdateDestroySupportRequestAPIView.as_view(),name="retrieve_update_destroy_support_request"),
]
