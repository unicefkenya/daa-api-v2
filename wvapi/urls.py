"""template URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

"""
from django.conf import settings
from django.conf.urls import url, include
from drf_autodocs.views import TreeView
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from wv_statistics.views import GetAllReport, Ping

urlpatternsv1 = [
    # url(r'^clients/',include('client.urlsV1')),
    # url(r'^games/',include('game.urlsV1')),
    url(r"^users/", include("client.urlsv1")),
    url(r"^attendances/", include("attendance.urlsv1")),
    url(r"^schools/", include("school.urlsv1")),
    url(r"^statistics/", include("wv_statistics.urlsv1")),
    url(r"^regions/", include("region.urlsv1")),
    url(r"^schools/", include("school.urlsv1")),
    url(r"^support-questions/", include("support_question.urlsv1")),
    url(r"^districts/", include("region.district.urlsv1")),
    url(r"^villages/", include("region.village.urlsv1")),
    url(r"^stats/", include("stats.urls")),
    url(r"^teachers/", include("school.teacher.urlsv1")),
    url(r"^streams/", include("school.stream.urlsv1")),
    url(r"^students/", include("school.student.urlsv1")),
    url(r"^promotions/", include("school.promotion.urlsv1")),
    # url("^exports/",include("stats.exports.urls")),
    url("^downloads/", include("stats.exports.urls")),
    url(r"^students-delete-reasons/", include("school.delete_reason.urlsv1")),
    url(r"^students-absent-reasons/", include("school.absent_reason.urlsv1")),
    url(r"^ping/?$", Ping.as_view(), name="ping_server"),
    url("^counties/", include("region.countys.urls")),
    url("^sub-counties/", include("region.sub_countys.urls")),
    url("^special-needs/", include("school.special_needs.urls")),
    url("^support-requests/", include("support_question.support_requests.urls")),
    url("^schools-imports/", include("school.schools_students_imports.urls")),
]
urlpatternsv2 = [
    url(r"^teacher-attendances/", include("attendance.v2.urls")),
]

# versions from the Apis(v1,v2)
apiversionsurlsparterns = [url(r"^v1/", include(urlpatternsv1)), url(r"^v2/", include(urlpatternsv2))]


urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^api/", include(apiversionsurlsparterns)),
    url(r"^o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    url(r"^auth/", include("rest_framework_social_oauth2.urls")),
    url(r"apiauth/", include("rest_framework.urls")),
    url(r"^$", TreeView.as_view(), name="api-tree"),
]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
print(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
