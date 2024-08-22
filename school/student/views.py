import json

from django.db.models import Count, Case, When, Q, Value, CharField, TextField, F, Prefetch
from django.db.models.functions import Concat, Cast
from django.db.models.functions import ExtractMonth, ExtractYear, TruncDate
from django.http.response import HttpResponseBase
from django_filters.rest_framework import DjangoFilterBackend
from drf_autodocs.decorators import format_docstring
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView

from attendance.filters import AttendanceFilter
from attendance.models import Attendance
from mylib.my_common import MyDjangoFilterBackend, MyCustomException, MyStandardPagination, FilterBasedOnRole
from region.models import SubCounty
from school.filters import BASE_STUDENT_REASON_FILTERS
from school.models import Student, StudentDeleteReason, Stream, STUDENTS_STATS_DEFINTIONS, STUDENTS_STATS_DEFAULT_FIELDS
from school.student.filters import EnrollmentFilter
from school.student.serializers import StudentSerializer, DeleteStudentSerializer, BulkStudentSerializer, EnrollmentSerializer, AbsentStudentSerializer
from stats.views import MyCustomDyamicStats
from django.contrib.auth import get_user_model

User=get_user_model()
 

class ListCreateStudentsAPIView(FilterBasedOnRole, generics.ListCreateAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all().prefetch_related(
        "special_needs",
        Prefetch("sub_county", queryset=SubCounty.objects.all().only("id", "name", "county_id").prefetch_related("county")),
        Prefetch("stream", queryset=Stream.objects.all().only("id", "name", "base_class", "school_id").prefetch_related("school")),
    )
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    filter_class = EnrollmentFilter
    pagination_class = MyStandardPagination

    def perform_create(self, serializer):
        serializer.save()


class ListEnrolmentByPartnerAPIView(generics.ListAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    filter_mixin = EnrollmentFilter
    
    def list(self, request, *args, **kwargs):
        partners=User.objects.filter(is_partner=True).values("id","filter_args","username")
        data=[]
      
        
        return Response({})
    
    

SUPPOERTED_STAT_TYES = [stat for stat in STUDENTS_STATS_DEFINTIONS]
@format_docstring({}, stat_types=", ".join(SUPPOERTED_STAT_TYES))
class ListStudentsDynamicsAPIView(MyCustomDyamicStats, generics.ListCreateAPIView):
    """
    Group statistics by:
    `type` = {stat_types}
    """

    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    filter_mixin = EnrollmentFilter
    stat_type = ""
    count_name = "total_students"
    stats_definitions = STUDENTS_STATS_DEFINTIONS
    default_fields = STUDENTS_STATS_DEFAULT_FIELDS
    
    
    def get_export_task_user(self):
        filters= super(ListStudentsDynamicsAPIView,self).get_possible_filters()
        partner_filter= filters.get("partner",None)
        if partner_filter==None:
            return super(ListStudentsDynamicsAPIView,self).get_export_task_user()
        return partner_filter.get("value")
    
    
    def get_possible_filters(self):
        filters= super(ListStudentsDynamicsAPIView,self).get_possible_filters()
        if "partner" in filters:
            filters.pop("partner")
        return filters
    

    def list(self, request, *args, **kwargs):
        # print("Umeanza ")
        # print(self.kwargs)
        # print(request.query_params)
        # print(self.request.user)
        return super(ListStudentsDynamicsAPIView, self).list(request, *args, **kwargs)


class GetStatsStudentsAPIView(FilterBasedOnRole, generics.ListCreateAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    filter_mixin = EnrollmentFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        res = queryset.aggregate(**STUDENTS_STATS_DEFAULT_FIELDS)
        return Response(res)


class ListCreateBulkStudents(FilterBasedOnRole, ListBulkCreateUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = BulkStudentSerializer
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    pagination_class = MyStandardPagination


class RetrieveUpdateDestroyStudentAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        params = self.request.query_params
        data = {"student": instance.id}
        if "reason" not in params:
            raise MyCustomException("Reason required..")
        data["reason"] = params.get("reason")
        if "description" in params:  # d
            data["description"] = params.get("description")
        ser = DeleteStudentSerializer(data=data)
        ser.is_valid(raise_exception=True)
        reason = ser.validated_data.get("reason")
        desc = ser.validated_data.get("description")
        if reason.name == "Error in Entry of Information":
            instance.delete()
            return Response({"detail": "Student deleted permanently."}, status=status.HTTP_204_NO_CONTENT)

        # Deactivate the student
        instance.active = False

        # Create the deletereason
        deletereason = StudentDeleteReason.objects.create(reason_id=reason.id, student_id=instance.id, description=desc)
        # print(deletereason.description)
        instance.save()
        return Response({"detail": "Student deactivated."}, status=status.HTTP_204_NO_CONTENT)


class GetStudentsEnrollment(FilterBasedOnRole, generics.ListAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = EnrollmentFilter
    # pagination_class = None
    nonefomats = ["class", "gender", "county", "village"]
    fakepaginate = False

    def list(self, request, *args, **kwargs):
        queryset = self.get_my_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        return EnrollmentSerializer

    def get_my_queryset(self):
        studs = self.filter_queryset(Student.objects.all())
        format = self.kwargs["type"]
        at = self.get_formated_data(studs, format=format)
        return at

    def resp_fields(self):
        # lst = str(datetime.now().date() - timedelta(days=365))
        # enrolledm = Count(Case(When(Q(date_enrolled__gte=lst) & Q(gender="M"), then=1), output_field=IntegerField(), ))
        enrolledm = Case(
            When(Q(gender="F") & Q(active=False), then=Value("dropout_females")),
            When(Q(gender="F") & Q(active=False), then=Value("dropout_females")),
            When(Q(gender="M") & Q(active=False), then=Value("dropout_males")),
            When(Q(gender="F") & Q(active=True), then=Value("females")),
            When(Q(gender="M") & Q(active=True), then=Value("males")),
            default=Value("others"),
            output_field=CharField(),
        )
        return enrolledm

    def get_formated_data(self, data, format):
        enrolledm = self.resp_fields()
        # enrolledm, oldf, enrolledf, oldm,dropoldm,dropoldf,dropnewm,dropnewf = self.resp_fields()
        outp = Concat("month", Value(""), output_field=CharField())
        at = (
            data.annotate(month=self.get_format(format=format))
            .values("month")
            .order_by(
                "month",
            )
            .annotate(type=enrolledm)
            .annotate(count=Count("id", distinct=True))
        )
        # at=self.append_extra_fields(at,format)
        return self.filter_formatted_data(format=format, data=at)

    def append_extra_fields(self, data, format):
        if format == "village":
            data = data
        return data

    def filter_formatted_data(self, format, data):
        return data.order_by("month")

    def group(self, data):
        data_dict = json.loads(json.dumps(data))
        values = [d["month"] for d in data_dict]
        values = list(set(values))
        output = []
        for a in values:
            if a == "":
                continue
            value_obj = {}
            value_obj["value"] = a
            # Try getting the value object
            value_objs = [p for p in data_dict if p["month"] == a]
            total_attrs = ["males", "females"]
            dropout_total_attrs = ["dropout_males", "dropout_females"]
            dropout_total = 0
            total = 0
            for b in value_objs:
                if b["type"] in total_attrs:
                    total += b["count"]
                elif b["type"] in dropout_total_attrs:
                    dropout_total += b["count"]
                value_obj[b["type"]] = b["count"]
            value_obj["total"] = total
            value_obj["dropout_total"] = dropout_total
            output.append(self.confirm_obj(value_obj))

        return sorted(output, key=lambda k: k.get("value", 0), reverse=False)

    def confirm_obj(self, obj):
        attrs = ["dropout_females", "dropout_males", "males", "females"]
        for at in attrs:
            try:
                obj[at]
            except:
                obj[at] = 0

        return obj

    def paginate_queryset(self, queryset):
        self.fakepaginate = True
        return None

    def finalize_response(self, request, response, *args, **kwargs):
        assert isinstance(response, HttpResponseBase), "Expected a `Response`, `HttpResponse` or `HttpStreamingResponse` " "to be returned from the view, but received a `%s`" % type(response)
        response.data = self.group(response.data)
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

    def get_format(self, format):
        daily = Concat(
            TruncDate("date_enrolled"),
            Value(""),
            output_field=CharField(),
        )
        monthly = Concat(
            ExtractYear("date_enrolled"),
            Value("-"),
            ExtractMonth("date_enrolled"),
            Value("-1"),
            output_field=CharField(),
        )

        # monthly= Concat(Value('1/'), ExtractMonth('date_enrolled'), Value('/'), ExtractYear("date_enrolled"),
        #               output_field=CharField(), )

        if format == "monthly":
            return monthly
        # elif format=="daily":
        #     return daily
        elif format == "yearly":
            return ExtractYear("date_enrolled")
        elif format == "village":
            return F("village")
        elif format == "school":
            return Concat("stream__school_id", Value("_"), F("stream__school__lat"), Value("_"), F("stream__school__lng"), Value("_"), F("stream__school__name"), output_field=CharField())
        elif format == "gender":
            return Value("gender", output_field=CharField())
        elif format == "school":
            id = Cast("stream__school_id", output_field=TextField())
            return Concat("stream__school__name", Value(","), id, output_field=CharField())
        elif format == "stream":
            return Concat("stream__name", Value(""), output_field=CharField())
        # elif format=="county":
        #     return Concat("stream__school__zone__subcounty__county__county_name",Value(''),output_field=CharField())
        elif format == "class":
            id = Cast("stream", output_field=TextField())
            return Concat("stream__base_class", Value(""), output_field=CharField())
        else:
            return monthly


class ListAbsentStudentsAPIView(FilterBasedOnRole, generics.ListAPIView):
    queryset = Attendance.objects.filter(status=0)
    filter_class = AttendanceFilter
    filter_backends = (DjangoFilterBackend,)
    serializer_class = AbsentStudentSerializer
    pagination_class = MyStandardPagination
    extra_filter_fields = BASE_STUDENT_REASON_FILTERS

    def list(self, request, *args, **kwargs):
        queryset = self.get_my_queryset()
        page = self.paginate_queryset(queryset)
        page = Student.objects.filter(active=True, id__in=page)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        # queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_my_queryset(self):
        # atts=Attendance.objects.all()
        atts = self.queryset.select_related("student", "stream")
        atts = self.filter_queryset(atts)
        return atts.values_list("student", flat=True)


class ListDropoutStudents(FilterBasedOnRole, generics.ListAPIView):
    queryset = StudentDeleteReason.objects.all().select_related("student", "student__stream", "student__stream__school")
    serializer_class = DeleteStudentSerializer
    pagination_class = MyStandardPagination
    filter_backends = (MyDjangoFilterBackend,)
    extra_filter_fields = BASE_STUDENT_REASON_FILTERS
