import django_filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from school.models import Stream
from school.permissions import IsAnEmptySteam
from school.stream.serializers import StreamSerializer
from mylib.my_common import MyDjangoFilterBackend, MyStandardPagination, FilterBasedOnRole
from django_filters.rest_framework import FilterSet


class StreamFilter(FilterSet):
    school = django_filters.NumberFilter(field_name="school_id", label="School Id")
    school_name = django_filters.CharFilter(field_name="school__name", label="School Name", lookup_expr="icontains")
    school_emis_code = django_filters.NumberFilter(field_name="school__emis_code", label="School emis code")

    class Meta:
        model = Stream
        exclude = ("moe_extra_info",)
        fields = "__all__"


class ListCreateStreamsAPIView(FilterBasedOnRole, generics.ListCreateAPIView):
    serializer_class = StreamSerializer
    queryset = Stream.objects.all().prefetch_related("school")
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    pagination_class = MyStandardPagination
    filter_mixin = StreamFilter

    def perform_create(self, serializer):
        serializer.save()


class RetrieveUpdateDestroyStreamAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StreamSerializer
    queryset = Stream.objects.all().select_related("school")
    permission_classes = (IsAuthenticated, IsAnEmptySteam)
