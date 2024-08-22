
from rest_framework import  generics
from school.models import SpecialNeed
from school.special_needs.serializers import SpecialNeedSerializer
from rest_framework.permissions import IsAuthenticated
from mylib.my_common import MyDjangoFilterBackend, MyStandardPagination

class ListCreateSpecialNeedsAPIView(generics.ListCreateAPIView):
    serializer_class = SpecialNeedSerializer
    queryset = SpecialNeed.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)

class RetrieveUpdateDestroySpecialNeedAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SpecialNeedSerializer
    queryset = SpecialNeed.objects.all()
    permission_classes = (IsAuthenticated,)
