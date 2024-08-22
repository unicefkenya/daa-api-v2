from django.conf.urls import url

from school.views import ListCreateSchoolsAPIView, RetrieveUpdateDestroySchoolAPIView
from wv_statistics.views import GetAllReport

urlpatterns=[
    url(r'^$',GetAllReport.as_view(),name="list_all_statistics"),
]