from django.shortcuts import render

# Create your views here.

from rest_framework import generics, status
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from django.db.models import F, Count, DateField, DateTimeField, CharField, IntegerField, Q
from django.db.models import Value
from django.db.models.functions import Concat
from django.db.models.functions import ExtractHour
from django.db.models.functions import ExtractMonth
from django.db.models.functions import ExtractYear
from django.db.models.functions import TruncDate
from django_filters.rest_framework import FilterSet,DjangoFilterBackend
import django_filters
from datetime import datetime

from mylib.my_common import MyDjangoFilterBackend, MyCustomException, MyStandardPagination
from school.models import Student
from school.promotion.filters import PromoteSchoolFilter
from school.promotion.models import PromoteSchool, PromoteStream
from school.promotion.serializers import PromoteSchoolSerializer


class CreateListPromoteSchool(generics.ListCreateAPIView):
    queryset = PromoteSchool.objects.all()
    serializer_class =PromoteSchoolSerializer
    filter_backends = (MyDjangoFilterBackend,)

    def get_serializer_class(self):
        # GraduatesStream.objects.all().delete()
        return PromoteSchoolSerializer



class RetrievePromoteSschool(generics.RetrieveUpdateAPIView):
    queryset = PromoteSchool.objects.all()
    serializer_class =PromoteSchoolSerializer

class CompletePromotionSerializer(serializers.Serializer):
    action=serializers.CharField(max_length=20)

class RetrieveCompletePromoteSschool(generics.CreateAPIView):
    queryset = PromoteSchool.objects.all()
    serializer_class =CompletePromotionSerializer

    def create(self, request, *args, **kwargs):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        ##Clue id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = {self.lookup_field: self.kwargs[lookup_url_kwarg]}["pk"]
        self.validate_promotion_id(id)
        promotion=PromoteSchool.objects.get(id=id)
        action=serializer.validated_data.get("action").lower()
        if action=="complete":
            if promotion.completed:
                raise MyCustomException("Already completed promotions", 400)
            promotion.complete()
        elif action=="undo":
            if not promotion.completed:
                raise MyCustomException("Undo is only for completed promotions", 400)
            promotion.undo()
        return Response(PromoteSchoolSerializer(promotion).data)

    def validate_promotion_id(self,id):
        if not PromoteSchool.objects.filter(id=id).exists():
            raise MyCustomException("Promotion Config does not exist",404)






class PromotionsStaisticsView(generics.ListCreateAPIView):
    queryset = PromoteSchool.objects.all()
    serializer_class = PromoteSchoolSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class=PromoteSchoolFilter

    formats = ["daily", "hourly", "monthly", "yearly", "radio", "device", "song", "country"]
    append_county_names = ["radio", "country"]
    format = None
    order_by = None
    pagination_class = MyStandardPagination

    def list(self, request, *args, **kwargs):
        self.order_by = self.request.query_params.get("order_by", None)
        queryset=""
        years=[d for d in range(2016,datetime.now().year+2)]
        print("The years ",years)
        stds=[]
        querysett= self.filter_queryset(self.get_queryset())
        for year in years:
            pids= querysett.filter(completed=True,year=year).values_list("id",flat=True)
            stream_ids=PromoteStream.objects.filter(promote_school_id__in=pids,completed=True).values_list("next_class",flat=True)
            dts=Student.objects.filter(stream_id__in=stream_ids).values("gender").annotate(count=Count("gender"))

            stds.append({
                "year":year,
                "data":dts
            })
        return Response(stds)


