from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from mylib.my_common import MyDjangoFilterBackend, MyStandardPagination, filter_queryset_based_on_role
from mylib.mygenerics import MyListAPIView
from region.serializers import RegionSerializer

