from django_filters.rest_framework import DjangoFilterBackend
from drf_autodocs.decorators import format_docstring
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from school.models import Teacher, TEACHER_STATS_DEFINITIONS, DEFAULT_TEACHER_FIELDS, School
from school.permissions import IsNonDeleteTeacher
from school.teacher.filters import TeacherFilter
from school.teacher.serializers import TeacherSerializer, TeacherSchoolInfoSerializer
from mylib.my_common import MyDjangoFilterBackend, MyStandardPagination, FilterBasedOnRole
from stats.views import MyCustomDyamicStats


class ListCreateTeachersAPIView(FilterBasedOnRole,generics.ListCreateAPIView):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class=TeacherFilter
    permission_classes = (IsAuthenticated,)
    pagination_class = MyStandardPagination

    def perform_create(self, serializer):
        serializer.save()


#
SUPPOERTED_STAT_TYES = [stat for stat in TEACHER_STATS_DEFINITIONS]
@format_docstring({}, stat_types=", ".join(SUPPOERTED_STAT_TYES))
class ListCreateTeachersDynamicsAPIView(MyCustomDyamicStats, generics.ListCreateAPIView):
    """
Group statistics by:
`type` = {stat_types}
        """
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    stat_type = ""
    filter_mixin=TeacherFilter
    count_name = "total_teachers"
    stats_definitions = TEACHER_STATS_DEFINITIONS
    default_fields=DEFAULT_TEACHER_FIELDS

    def create(self, request, *args, **kwargs):
      data=request.data.copy()
      school=data.get("school")
      # print(data)
      if not School.objects.filter(id=school).exists():
        if Teacher.objects.filter(id=school).exists():
              data["school"]=Teacher.objects.get(id=school).school_id

      # print(data)
      serializer = self.get_serializer(data=data)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      headers = self.get_success_headers(serializer.data)
      return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)







class RetrieveUpdateDestroyTeacherAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    permission_classes = (IsAuthenticated,IsNonDeleteTeacher,)



class RetrieveSchoolInfoAPIView(generics.RetrieveAPIView):
    serializer_class = TeacherSchoolInfoSerializer
    queryset = Teacher.objects.all().select_related("school",)
    permission_classes = (IsAuthenticated,IsNonDeleteTeacher,)


    def get_object(self):
        ##Get the techer based on the request user
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"user_id": self.request.user.id}
        obj = get_object_or_404(queryset, **filter_kwargs)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        # print(obj.)
        return obj
