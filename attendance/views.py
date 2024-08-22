from django.db import transaction
from django.db.models import Q, Value, DateTimeField, OuterRef, Subquery
from django.db.models.functions import Concat, Trunc
from django.http.response import HttpResponseBase
from django.shortcuts import render
from datetime import datetime

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.filters import AttendanceFilter
from attendance.permission import IsTeacherOfTheSchool
from attendance.signals import attendance_taken_signal
from mylib.my_common import (
    FilterBasedOnRole,
    MyDjangoFilterBackend,
    MyStandardPagination,
    str2bool,
    MyCustomException,
)
from attendance.models import (
    ATTENDANCE_STATS_DEFAULT_FIELDS,
    ATTENDANCE_STATS_DEFINTIONS,
    Attendance,
    AttendanceHistory,
)
from attendance.serializers import (
    AttendanceSerializer,
    TakeAttendanceSerializer,
    SerializerAllPercentages,
    SerializerAll,
    StreamAttendanceSerializer,
)
from school.models import Student, Stream
from stats.serializers import BaseDynamicStatsSerializer
from drf_autodocs.decorators import format_docstring
from stats.views import MyCustomDyamicStats
import hashlib

from django.db.models import (
    Count,
    Case,
    When,
    IntegerField,
    Q,
    Value,
    CharField,
    Sum,
    Avg,
    BooleanField,
    DateField,
    F,
)
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractDay, TruncDate
from django.db.models.functions import Concat, Cast
from django.utils.dateparse import parse_date


class ListCreateAttendancesAPIView(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    pagination_class = MyStandardPagination


def days_between(d1, d2):
    try:
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        return abs((d2 - d1).days)
    except ValueError:
        ##Return a big number if either of the dates has an error
        return 100000


ATTENDANCE_SUPPOERTED_STAT_TYES = [stat for stat in ATTENDANCE_STATS_DEFINTIONS]


@format_docstring({}, stat_types=", ".join(ATTENDANCE_SUPPOERTED_STAT_TYES))
class ListAttendanceDynamicStatisticsAPIView(MyCustomDyamicStats, generics.ListAPIView):
    """
    Group statistics by:
    `type` = {stat_types}
    """

    serializer_class = BaseDynamicStatsSerializer
    queryset = Attendance.objects.annotate(gender=F("student__gender")).select_related(
        "student"
    )
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    stat_type = ""
    filter_mixin = AttendanceFilter
    count_name = "total_attendances_taken"
    stats_definitions = ATTENDANCE_STATS_DEFINTIONS
    default_fields = ATTENDANCE_STATS_DEFAULT_FIELDS

    def get_stats_cache_key(self):
        key = self.request.get_raw_uri()
        user_id = 0
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        final_key = f"{key}_{user_id}"
        result = hashlib.md5(final_key.encode()).hexdigest()
        return result

    def get_queryset(self):
        self.get_stats_cache_key()

        return super(ListAttendanceDynamicStatisticsAPIView, self).get_queryset()

    def get_export_task_user(self):
        filters = super(
            ListAttendanceDynamicStatisticsAPIView, self
        ).get_possible_filters()
        partner_filter = filters.get("partner", None)
        if partner_filter == None:
            return super(
                ListAttendanceDynamicStatisticsAPIView, self
            ).get_export_task_user()
        return partner_filter.get("value")

    """
     - Partner filter is a method filter thus cannot be used for exports as it's not a field
    """

    def get_possible_filters(self):
        filters = super(
            ListAttendanceDynamicStatisticsAPIView, self
        ).get_possible_filters()
        if "partner" in filters:
            filters.pop("partner")
        return filters


class GetStatsAttendanceAPIView(FilterBasedOnRole, generics.ListCreateAPIView):
    serializer_class = BaseDynamicStatsSerializer
    queryset = Attendance.objects.annotate(gender=F("student__gender")).select_related(
        "student"
    )
    filter_mixin = AttendanceFilter
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        res = queryset.aggregate(**ATTENDANCE_STATS_DEFAULT_FIELDS)
        return Response(res)


class RetrieveUpdateDestroyAttendanceAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()


class BulkListCreateAttendances(generics.CreateAPIView):
    pass


class ListCreateStreamAttendance(generics.ListCreateAPIView):
    permission_classes = (IsTeacherOfTheSchool,)
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_class = AttendanceFilter
    pagination_class = MyStandardPagination

    def create(self, request, *args, **kwargs):
        bulk = isinstance(request.data, list)
        if bulk:
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # print("")
        return Response(serializer.data, 201)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return StreamAttendanceSerializer
        return self.serializer_class


class ListCreateAttendanceStatistics(generics.ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = AttendanceFilter
    pagination_class = MyStandardPagination
    nonefomats = [
        "yearly",
        "class",
        "monthly",
        "village",
        "school",
        "gender",
        "county",
        "oosc",
        "partner",
        "school",
    ]
    fakepaginate = False

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        theformat = self.kwargs["type"]
        startdate = self.request.query_params.get("start_date", "2017-04-01")
        enddate = self.request.query_params.get(
            "end_date", datetime.now().strftime("%Y-%m-%d")
        )
        pagesize = int(self.request.query_params.get("page_size", 200))
        if theformat in self.nonefomats:
            self.fakepaginate = True
            return None
        elif startdate != None and days_between(startdate, enddate) <= pagesize:
            # print (days_between(startdate,enddate),days_between(startdate,enddate) <= pagesize)
            self.fakepaginate = True
            return None
        elif (
            theformat == "weekly"
            and startdate != None
            and days_between(startdate, enddate) / 5 <= pagesize
        ):
            # print ("weekly",days_between(startdate, enddate)/5, days_between(startdate, enddate)/5 <= pagesize)
            self.fakepaginate = True
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def finalize_response(self, request, response, *args, **kwargs):
        assert isinstance(response, HttpResponseBase), (
            "Expected a `Response`, `HttpResponse` or `HttpStreamingResponse` "
            "to be returned from the view, but received a `%s`" % type(response)
        )

        # If it does not use pagination and require fake pagination for response
        if self.fakepaginate:
            data = response.data
            resp = {}
            resp["count"] = len(data)
            resp["next"] = None
            resp["prev"] = None
            resp["results"] = data
            response.data = resp
        # print (response.data)
        if isinstance(response, Response):
            if not getattr(request, "accepted_renderer", None):
                neg = self.perform_content_negotiation(request, force=True)
                request.accepted_renderer, request.accepted_media_type = neg
            response.accepted_renderer = request.accepted_renderer
            response.accepted_media_type = request.accepted_media_type
            response.renderer_context = self.get_renderer_context()

        for key, value in self.headers.items():
            response[key] = value
        return response

    # def get_pagination_class(self):
    #     print("Getting the format")
    #     theformat = self.kwargs['type']
    #     nonefomats=["yearly","class"]
    #     if theformat in nonefomats:
    #         return None
    #     return StandardresultPagination

    # def list(self, request, *args, **kwargs):

    def list(self, request, *args, **kwargs):
        queryset = self.get_my_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_my_queryset(self):
        # atts=Attendance.objects.all()
        atts = Attendance.objects.select_related("student", "stream")
        atts = self.filter_queryset(atts)
        format = self.kwargs["type"]
        at = self.get_formated_data(atts, format=format)
        # at["present_males"]=float(at["present_males"])/total

        return at

    def get_serializer_context(self):
        ####print("setting the context")
        student = self.request.query_params.get("student", None)
        return_type = self.request.query_params.get("return_type", None)
        return {
            "type": self.kwargs["type"],
            "student": student,
            "return_type": return_type,
        }

    def get_serializer_class(self):
        if self.request.method == "GET":
            format = self.kwargs["type"]
            if format != "daily":
                return SerializerAllPercentages
            print("Getting the all percentages....")
            return SerializerAll

        elif self.request.method == "POST":
            return AttendanceSerializer

    def resp_fields(self):
        pm = Count(
            Case(
                When(
                    Q(student__gender="M") & Q(status=1) & Q(student__active=True),
                    then=1,
                ),
                output_field=IntegerField(),
            )
        )
        pf = Count(
            Case(
                When(
                    Q(student__gender="F") & Q(status=1) & Q(student__active=True),
                    then=1,
                ),
                output_field=IntegerField(),
            )
        )
        af = Count(
            Case(
                When(
                    Q(student__gender="F") & Q(status=0) & Q(student__active=True),
                    then=1,
                ),
                output_field=IntegerField(),
            )
        )
        am = Count(
            Case(
                When(
                    Q(student__gender="M") & Q(status=0) & Q(student__active=True),
                    then=1,
                ),
                output_field=IntegerField(),
            )
        )
        return pm, pf, af, am

    def get_formated_data(self, data, format):
        pm, pf, af, am = self.resp_fields()
        outp = Concat("month", Value(""), output_field=CharField())
        at = data.annotate(month=self.get_format(format=format)).values("month")
        at = at.annotate(
            present_males=pm,
            present_females=pf,
            absent_males=am,
            absent_females=af,
            value=F("month"),
        )
        # at=at.annotate(value=Concat(Value(queryet),Value(""),output_field=CharField()))
        # #print (at)
        at = at.exclude(
            present_males=0, present_females=0, absent_males=0, absent_females=0
        )
        return self.filter_formatted_data(format=format, data=at)

    def filter_formatted_data(self, format, data):
        # if format=="monthly":
        #     return sorted(data,key=lambda x: x["value"], reverse=True)
        return data.order_by("value")

    def get_format(self, format):
        daily = Trunc("date", "day", output_field=DateField())
        monthly = Trunc("date", "month", output_field=DateField())
        weekly = Trunc("date", "week", output_field=DateField())

        if format == "monthly":
            return monthly
        elif format == "daily":
            return daily
        elif format == "village":
            return F("student__village")

        elif format == "school":
            return Concat(
                "stream__school_id",
                Value("_"),
                F("stream__school__lat"),
                Value("_"),
                F("stream__school__lng"),
                Value("_"),
                F("stream__school__name"),
                output_field=CharField(),
            )
        elif format == "weekly":
            return weekly
        elif format == "yearly":
            return ExtractYear("date")
        elif format == "stream":
            return Concat(
                "stream__base_class",
                Value("_"),
                F("stream__name"),
                Value("_"),
                F("stream__id"),
                output_field=CharField(),
            )
        # elif format=="partner":
        #     return Concat("student__class_id__school__partners",Value('-'),"student__class_id__school__partners__name",output_field=CharField())
        # elif format =="county":
        #     return Concat("_class__school__zone__subcounty__county__county_name",Value(''),output_field=CharField())
        elif format == "class":
            return Concat("stream__base_class", Value(""), output_field=CharField())
        # elif format=="oosc":
        #     return Concat("student__is_oosc",Value(''),output_field=BooleanField())
        elif format == "gender":
            return F("student__gender")
            # return Concat("student__gender",Value(""),output_field=CharField())

        elif format == "school":
            return Concat(
                "stream__school__name",
                Value("_"),
                F("stream__school_id"),
                output_field=CharField(),
            )
        else:
            # #print daily
            return daily


# class MonitoringAttendanceTaking(generics.ListAPIView):
#     queryset = Stream.objects.all()
#     serializer_class = GetAttendanceHistorySerilizer
#     filter_backends = (DjangoFilterBackend,)
#     filter_class=StreamFilter
#     allowed_order_by=["school","attendance_count"]
#
#     def get_queryset(self):
#         start_date,end_date,attendance_taken=self.parse_querparams()
#         print ('%s to %s'%(start_date,end_date))
#
#         ###Get the days attendace was expected
#         days=get_list_of_dates(start_date=start_date,end_date=end_date)
#         total_days=len(days)
#         # print (total_days)
#
#         ###Get order by
#         order_by=self.request.GET.get("order_by",None)
#         if order_by not in self.allowed_order_by:order_by="attendance_count"
#
#         atts=AttendanceHistory.objects.all()
#         streams=self.filter_queryset(self.queryset)
#         days = [d.date() for d in days]
#         print(days)
#         atts=atts.filter(_class_id=OuterRef("id")).filter(date__in=days).annotate(theclass=F("_class")).values("_class").\
#             annotate(count=Count("_class")).values_list("count",flat=True)
#
#         ###Annoatate the data
#         streams=streams.annotate(attendance_count=Subquery(atts[:1],output_field=IntegerField()),
#                                  total_days=Value(total_days,output_field=IntegerField()),
#                                  school_name=F("school__school_name"),
#                                 school_type=F("school__status"),
#                                 school_emis_code=F("school__emis_code"),
#                                  ).values("id","attendance_count","class_name","total_days","school_name","school_emis_code","school_type")\
#
#
#         ###Order_by
#         if order_by =="school":
#             streams=streams.order_by("school_name","-attendance_count","class_name")
#         else:
#             streams = streams.order_by( "-attendance_count","school_name","class_name")
#
#         if  attendance_taken:
#             return streams.filter(attendance_count__gte=0)
#         else:
#             return streams.filter(attendance_count__isnull=True)
#
#     def parse_querparams(self):
#         start_date = self.request.GET.get("start_date", None)
#         end_date = self.request.GET.get("end_date", None)
#         taken_attendance = self.request.GET.get("taken_attendance", None)
#         if start_date == None or end_date == None or taken_attendance ==None: raise MyCustomException(
#             "You must include the `start_date` , `end_date` , `taken_attendance` in the query params");
#         print ("taken_attendance",taken_attendance)
#         return start_date,end_date,str2bool(taken_attendance)
