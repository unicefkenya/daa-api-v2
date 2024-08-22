from django.conf.urls import url

from region.district.views import ListCreateDistrictsAPIView, RetrieveUpdateDestroyDistrictAPIView, \
    ListCreateDistrictVillages

urlpatterns=[
    url(r'^$',ListCreateDistrictsAPIView.as_view(),name="list_create_districts"),
    url(r'^(?P<pk>[0-9]+)/?$',RetrieveUpdateDestroyDistrictAPIView.as_view(),name="retrieve_update_destroy_district"),
    url(r'^(?P<pk>[0-9]+)/villages/?$', ListCreateDistrictVillages.as_view(), name="list_district_villages"),

]