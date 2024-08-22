
from django.conf.urls import url
from school.schools_students_imports.views import ListCreateSchoolsStudentsImportsAPIView, RetrieveUpdateDestroySchoolsStudentsImportAPIView
urlpatterns=[
    url(r'^$',ListCreateSchoolsStudentsImportsAPIView.as_view(),name="list_create_schools_students_imports"),
    url(r'^(?P<pk>[0-9]+)/?$',RetrieveUpdateDestroySchoolsStudentsImportAPIView.as_view(),name="retrieve_update_destroy_schools_students_import"),
]
