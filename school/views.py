import csv
import gc
import json
from sys import stdout

from django.db.models import Q
from django.http import StreamingHttpResponse
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from drf_autodocs.decorators import format_docstring
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from time import sleep, timezone

from rest_framework.response import Response
from rest_framework.views import APIView


from mylib.my_common import MyDjangoFilterBackend, MyStandardPagination, MyCustomException, FilterBasedOnRole
from mylib.mygenerics import MyListAPIView
from core.reports.overall import OverAllReport
from school.filters import SchoolFilter
from school.models import School, Student, SCHOOL_STATS_DEFINITIONS, DEFAULT_SCHOOL_FIELDS
from school.serializers import SchoolSerializer, ImportStudentSerializer, SchoolImportError, ImportErrorSerializer, ImportResultsSerializer, ImportResults
from stats.views import MyCustomDyamicStats


class ListCreateSchoolsAPIView(FilterBasedOnRole, generics.ListCreateAPIView):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (MyDjangoFilterBackend,)
    pagination_class = MyStandardPagination


SUPPOERTED_STAT_TYES = [stat for stat in SCHOOL_STATS_DEFINITIONS]


@format_docstring({}, stat_types=", ".join(SUPPOERTED_STAT_TYES))
class ListCreateSchoolsDynamicsAPIView(MyCustomDyamicStats, generics.ListCreateAPIView):
    """
    Group statistics by:
    `type` = {stat_types}
    """

    serializer_class = SchoolSerializer
    queryset = School.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    filter_mixin = SchoolFilter
    permission_classes = (IsAuthenticated,)
    count_name = "total_schools"
    stats_definitions = SCHOOL_STATS_DEFINITIONS
    default_fields = DEFAULT_SCHOOL_FIELDS


from stats.models import Export
from django.utils import dateparse, timezone

from datetime import datetime
from django.apps import apps


class APIReportHtmVIew(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        report = OverAllReport("onekana_report.html")
        #  "name",
        #     "title",
        #     "description",
        #     "start_time",
        #     "end_time",
        user_model = apps.get_model("client", "MyUser")

        export = Export(
            title="Onekana Report June",
            name="Hello",
            custom_report_name="overall",
            user=user_model.objects.filter(username="myadmin").first(),
            start_date=datetime(2018, 4, 1),
            end_date=timezone.now(),
            description="Attendance report, Enrollment",
        )
        export.save()
        return render(request, report.template, report.get_context(export))


class RetrieveUpdateDestroySchoolAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()


class ImportSchoolData(APIView):
    total_success = 0
    total_fails = 0
    total_duplicates = 0
    is_oosc = False

    def post(self, request, format=None):
        file = ""
        try:
            file = request.FILES["file"]
        except:
            raise MyCustomException("No .csv files sent.")
        if file:
            data = [row for row in csv.reader(file.read().decode("utf-8").splitlines())][1:]
        results = self.import_data(data)

        return Response(results)

    def import_data(self, data):
        total_success = 0
        total_fails = 0
        errors = []
        total = len(data)
        students = []

        for i, dat in enumerate(data):
            if total > 0:
                thep = (i + 1) / float(total)
                percentage = str(int(thep * 100)) + "%"
                stdout.write("\rImporting %s " % percentage)
                stdout.flush()
            dt = {"first_name": dat[3], "middle_name": dat[5], "last_name": dat[4], "emis_code": dat[2], "admission_no": dat[6], "stream": dat[7], "gender": dat[8], "base_class": dat[7]}
            ser = ImportStudentSerializer(data=dt)

            if not ser.is_valid():
                self.total_fails += 1
                # Adding 2 to row error due to header plus header is removed
                error = SchoolImportError(i + 2, ser.errors, json.dumps(dt))
                errors.append(error)
                continue
            stud = self.get_student(ser.validated_data)
            if stud:
                students.append(stud)

        try:
            resa = Student.objects.bulk_create(students)
            self.total_success = len(resa)
        except Exception as e:
            print(e)

        res = ImportResults(ImportErrorSerializer(errors, many=True).data, self.total_success, self.total_fails, self.total_duplicates)
        dt = ImportResultsSerializer(res).data
        return dt

    def get_student(self, data):
        if Student.objects.filter(first_name=data.get("first_name"), middle_name=data.get("middle_name"), last_name=data.get("last_name"), stream_id=data.get("stream")).exists():
            self.total_duplicates += 1
            return None

        return Student(
            first_name=data.get("first_name"),
            middle_name=data.get("middle_name"),
            last_name=data.get("last_name"),
            admission_no=data.get("admission_no"),
            gender=data.get("gender"),
            stream_id=data.get("stream"),
        )


class MoeTestSchool(APIView):
    def post(self, request, format=None):
        # syncMoeAllSchools()
        return Response({"detail": "ok"})


# class ExxportSchoolData(generics.ListAPIView):
#     def list(self, request, *args, **kwargs):
#         response = StreamingHttpResponse(
#             self.stream(), content_type='text/csv'
#         )
#         disposition = "attachment; filename=file.csv"
#         response['Content-Disposition'] = disposition
#         return response
#
#     def stream(self):
#         buffer_ = StringIO.StringIO()
#         writer = csv.writer(buffer_)
#         for row in School:
#             writer.writerow(row)
#             buffer_.seek(0)
#             data = buffer_.read()
#             buffer_.seek(0)
#             buffer_.truncate()
#             yield data

# class ListSchoolDistricts(MyListAPIView):
#     foreign_key_field="school"
#     queryset = District.objects.all()
#     serializer_class =DistrictSerializer
#     filter_backends = (MyDjangoFilterBackend,)
#     permission_classes = (IsAuthenticated,)
