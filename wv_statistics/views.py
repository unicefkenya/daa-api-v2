from django.db.models import Q, When, Value, Case, CharField, Count
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from mylib.my_common import filter_queryset_based_on_role
from school.models import Student, School, Teacher


class GetAllReport(APIView):
    def get(self, request, format=None):
        students = filter_queryset_based_on_role(Student.objects.all(), self.request.user.id)
        schools = filter_queryset_based_on_role(School.objects.all(), self.request.user.id)
        teachers = filter_queryset_based_on_role(Teacher.objects.all(), self.request.user.id)

        school = request.query_params.get("school", None)
        county = request.query_params.get("county", None)
        partner_admin = request.query_params.get("partner_admin", None)

        if school:
            students = students.filter(stream__school_id=school)
            schools = schools.filter(id=school)
            teachers = teachers.filter(school_id=school)

        activeschools = schools.filter(streams__isnull=False)

        sts = list(
            students.order_by()
            .annotate(
                type=Case(
                    When(Q(gender="F") & Q(active=False), then=Value("dropout_old_females")),
                    When(Q(gender="M") & Q(active=False), then=Value("dropout_old_males")),
                    When(Q(gender="F") & Q(active=True), then=Value("old_females")),
                    When(Q(gender="M") & Q(active=True), then=Value("old_males")),
                    default=Value("others"),
                    output_field=CharField(),
                )
            )
            .values("type")
            .annotate(count=Count("type"))
        )
        oosc_studs = (
            students.filter(active=True)
            .exclude(status="PE")
            .aggregate(
                ne_males=Count("id", filter=Q(status="NE", gender="M")),
                ne_females=Count("id", filter=Q(status="NE", gender="F")),
                oosc_females=Count("id", filter=Q(status="OOSC", gender="F")),
                oosc_males=Count("id", filter=Q(status="OOSC", gender="M")),
            )
        )
        # print(oosc_studs)

        mstudents = self.get_count(sts, "old_males")  # students.filter(gender="M").count()
        fstudents = self.get_count(sts, "old_females")  # students.filter(gender="F").count()
        mdropouts = self.get_count(sts, "dropout_old_males")  # students.filter(gender="M").count()
        fdropouts = self.get_count(sts, "dropout_old_females")  # students.filter(gender="F").count()

        activeschools = activeschools.distinct().count()
        teachers = teachers.count()
        schools = schools.count()

        return Response(
            data={
                "schools": schools,
                "active_schools": activeschools,
                "teachers": teachers,
                "students": {
                    **oosc_studs,
                    "males": mstudents,
                    "females": fstudents,
                    "dropout_males": mdropouts,
                    "dropout_females": fdropouts,
                },
            }
        )

    def get_count(self, list, item):
        obs = [g["count"] for g in list if g["type"] == item]
        if len(obs) > 0:
            return obs[0]
        return 0


class Ping(generics.ListCreateAPIView):
    def list(self, request, *args, **kwargs):
        return Response({"detail": "OK"})
