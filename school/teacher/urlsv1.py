from django.conf.urls import url

from school.teacher.views import ListCreateTeachersAPIView, RetrieveUpdateDestroyTeacherAPIView, \
    RetrieveSchoolInfoAPIView, ListCreateTeachersDynamicsAPIView

urlpatterns=[
    url(r'^$',ListCreateTeachersDynamicsAPIView.as_view(),name="list_create_teachers"),
    url(r'^(?P<pk>[0-9]+)/?$',RetrieveUpdateDestroyTeacherAPIView.as_view(),name="retrieve_update_destroy_teacher"),
    url(r'^stats/(?P<type>.+)', ListCreateTeachersDynamicsAPIView.as_view(), name="list_create_teachers_stats"),

    # url(r'^(?P<pk>[0-9]+)/school-info?$',RetrieveSchoolInfoAPIView.as_view(),name="retrieve_teacher_school_info"),
]