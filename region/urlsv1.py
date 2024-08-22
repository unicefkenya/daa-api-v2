from django.conf.urls import url

from region.views import ListCreateRegionsAPIView, RetrieveUpdateDestroyRegionAPIView, ListRegionDistricts

urlpatterns=[
    url(r'^$',ListCreateRegionsAPIView.as_view(),name="list_create_regions"),
    url(r'^(?P<pk>[0-9]+)/?$',RetrieveUpdateDestroyRegionAPIView.as_view(),name="retrieve_update_destroy_region"),
    url(r'^(?P<pk>[0-9]+)/districts/?$', ListRegionDistricts.as_view(), name="list_region_districts"),

]