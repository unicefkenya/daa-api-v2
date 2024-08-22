from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from mylib.mygenerics import MyListAPIView
from region.models import District, Village
from region.district.serializers import DistrictSerializer
from mylib.my_common import MyDjangoFilterBackend, MyStandardPagination
from region.village.serializers import VillageSerializer


class ListCreateDistrictsAPIView(generics.ListCreateAPIView):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    pagination_class = MyStandardPagination

    def perform_create(self, serializer):
        serializer.save()


class RetrieveUpdateDestroyDistrictAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()


class ListCreateDistrictVillages(MyListAPIView):
    foreign_key_field="district"
    queryset = Village.objects.all()
    serializer_class =VillageSerializer
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    pagination_class = MyStandardPagination