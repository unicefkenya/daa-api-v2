
from django.conf.urls import url
from region.countys.views import ListCreateCountysAPIView, RetrieveUpdateDestroyCountyAPIView
urlpatterns=[
    url(r'^$',ListCreateCountysAPIView.as_view(),name="list_create_countys"),
    url(r'^(?P<pk>[0-9]+)/?$',RetrieveUpdateDestroyCountyAPIView.as_view(),name="retrieve_update_destroy_county"),
]
