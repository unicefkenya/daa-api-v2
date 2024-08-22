from rest_framework import generics
from client.models import SCHOOL_ADMIN
from region.models import County
from region.countys.serializers import CountySerializer
from rest_framework.permissions import IsAuthenticated
from mylib.my_common import MyDjangoFilterBackend, MyStandardPagination, filter_queryset_based_on_role
from school.models import School


class ListCreateCountysAPIView(generics.ListCreateAPIView):
    serializer_class = CountySerializer
    queryset = County.objects.all().prefetch_related("sub_counties")
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryser = super(ListCreateCountysAPIView, self).get_queryset()
        return filter_queryset_based_on_role(queryset=queryser, user_id=self.request.user.id)

    # def get_queryset(self):
    #     queryset=super(ListCreateCountysAPIView,self).get_queryset()
    #     user=self.request.user
    #     filter_arg=user.filter_args
    #     if user.role=="A":
    #         return queryset
    #     elif user.role==SCHOOL_ADMIN:
    #         school=School.objects.get(id=filter_arg)
    #         return queryset.filter()

    #     return queryset


class RetrieveUpdateDestroyCountyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CountySerializer
    queryset = County.objects.all()
    permission_classes = (IsAuthenticated,)
