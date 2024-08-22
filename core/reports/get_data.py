# from django.http import HttpRequest

from asyncio import constants
import traceback
import requests
from rest_framework.reverse import reverse
from django.http import HttpRequest
from attendance.views import ListAttendanceDynamicStatisticsAPIView, GetStatsAttendanceAPIView
from school.student.views import GetStatsStudentsAPIView, ListStudentsDynamicsAPIView
from django.apps import apps

from wv_statistics.views import GetAllReport
def get_any_view(view, grouping, pass_grouping_kwarg=True, is_list=True, **kwargs):
    new_request = HttpRequest()
    new_request.method = "GET"
    new_request.user = kwargs.get("user")
    new_request.META["SERVER_NAME"] = "localhost"
    new_request.META["SERVER_PORT"] = 9000
    new_request.path = f"/a/{grouping}/?hana=oiiew"
    new_request.GET = {
        **kwargs.get("query_params", {}),
        **kwargs.get("order_by", {}),
        "is_training_school": False,
    }
    other_view = view.as_view()
    view_kwargs = {}
    if pass_grouping_kwarg:
        view_kwargs = {"type": grouping}
    response = other_view(new_request, **view_kwargs)
    # print("Am done")

    data = []
    # Process the response
    if response.status_code == 200:
        # Do something with the response
        # if is_list:
        #     data = response.data["results"]
        # else:
        data = response.data

    else:
        # print(response.status_code)
        print(response)
        data = []
        # Handle the error
    return data


def get_enrollment_stats_view(grouping, **kwargs):
    kwargs["order_by"] = {
        "order": "DESC",
        "order_by": "total_students",
        "active": True,
    }
    return get_any_view(ListStudentsDynamicsAPIView, grouping, **kwargs)


def get_attendance_stats_view(grouping, **kwargs):
    kwargs["order_by"] = {
        "order": "DESC",
        "order_by": "total_attendances_taken",
    }
    return get_any_view(ListAttendanceDynamicStatisticsAPIView, grouping, **kwargs)


def get_all_stats_view(grouping, **kwargs):
    kwargs["order_by"] = {}
    return get_any_view(GetAllReport, grouping, pass_grouping_kwarg=False, is_list=False, **kwargs)


def get_all_students_view(grouping, **kwargs):
    kwargs["order_by"] = {
        "active": True,
    }
    return get_any_view(GetStatsStudentsAPIView, grouping, pass_grouping_kwarg=False, is_list=False, **kwargs)


def get_all_attendances_view(grouping, **kwargs):
    kwargs["order_by"] = {}
    return get_any_view(GetStatsAttendanceAPIView, grouping, pass_grouping_kwarg=False, is_list=False, **kwargs)


def get_any_stats(model="students", grouping="county", **kwargs):
    return {
        "students": get_enrollment_stats_view,
        "attendances": get_attendance_stats_view,
        "all": get_all_stats_view,
        "all_students": get_all_students_view,
        "all_attendances": get_all_attendances_view,
    }[model](grouping, **kwargs)
