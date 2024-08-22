from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from mylib.my_common import MyDjangoFilterBackend, MyStandardPagination
from mylib.mygenerics import MyListAPIView
from support_question.models import SupportQuestion
from support_question.serializers import SupportQuestionSerializer

class ListCreateSupportQuestionsAPIView(generics.ListCreateAPIView):
    serializer_class = SupportQuestionSerializer
    queryset = SupportQuestion.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (MyDjangoFilterBackend,)
    pagination_class = MyStandardPagination



class RetrieveUpdateDestroySupportQuestionAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SupportQuestionSerializer
    queryset = SupportQuestion.objects.all()

    

# class ListSupportQuestionDistricts(MyListAPIView):
#     foreign_key_field="support_question"
#     queryset = District.objects.all()
#     serializer_class =DistrictSerializer
#     filter_backends = (MyDjangoFilterBackend,)
#     permission_classes = (IsAuthenticated,)
