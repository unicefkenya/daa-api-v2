
from django.conf.urls import url
from school.special_needs.views import ListCreateSpecialNeedsAPIView, RetrieveUpdateDestroySpecialNeedAPIView
urlpatterns=[
    url(r'^$',ListCreateSpecialNeedsAPIView.as_view(),name="list_create_special_needs"),
    url(r'^(?P<pk>[0-9]+)/?$',RetrieveUpdateDestroySpecialNeedAPIView.as_view(),name="retrieve_update_destroy_special_need"),
]
