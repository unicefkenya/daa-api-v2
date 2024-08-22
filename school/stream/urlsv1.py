from django.conf.urls import url

from school.stream.views import ListCreateStreamsAPIView, RetrieveUpdateDestroyStreamAPIView

urlpatterns=[
    url(r'^$',ListCreateStreamsAPIView.as_view(),name="list_create_streams"),
    url(r'^(?P<pk>[0-9]+)/?$',RetrieveUpdateDestroyStreamAPIView.as_view(),name="retrieve_update_destroy_stream"),
]