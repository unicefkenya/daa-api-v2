from django.conf.urls import url

from region.village.views import ListCreateVillagesAPIView, RetrieveUpdateDestroyVillageAPIView

urlpatterns=[
    url(r'^$',ListCreateVillagesAPIView.as_view(),name="list_create_villages"),
    url(r'^(?P<pk>[0-9]+)/?$',RetrieveUpdateDestroyVillageAPIView.as_view(),name="retrieve_update_destroy_village"),
]