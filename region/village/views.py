from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from region.models import Village
from region.village.serializers import VillageSerializer
from mylib.my_common import MyDjangoFilterBackend, MyStandardPagination


class ListCreateVillagesAPIView(generics.ListCreateAPIView):
    serializer_class = VillageSerializer
    queryset = Village.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    pagination_class = MyStandardPagination

    def perform_create(self, serializer):
        serializer.save()


class RetrieveUpdateDestroyVillageAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VillageSerializer
    queryset = Village.objects.all()