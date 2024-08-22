
from rest_framework import generics, status
from rest_framework.response import Response

from school.models import School, Teacher
from support_question.models import SupportRequest
from support_question.support_requests.serializers import SupportRequestSerializer
from rest_framework.permissions import IsAuthenticated
from mylib.my_common import MyDjangoFilterBackend, MyStandardPagination

class ListCreateSupportRequestsAPIView(generics.ListCreateAPIView):
    serializer_class = SupportRequestSerializer
    queryset = SupportRequest.objects.all()
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)

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

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

class RetrieveUpdateDestroySupportRequestAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SupportRequestSerializer
    queryset = SupportRequest.objects.all()
    permission_classes = (IsAuthenticated,)
