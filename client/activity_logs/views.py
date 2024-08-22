from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response

from client.activity_logs.filters import LogsFilter
from client.activity_logs.serializers import ActivityLogSerializer, ExportActivityLogSerializer
from client.models import ActivityLog
from mylib.my_common import MyDjangoFilterBackend
from mylib.queryset2excel import exportcsv


class ListActivityLogs(generics.ListAPIView):
    queryset = ActivityLog.objects.all().select_related("user")
    serializer_class = ActivityLogSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class=LogsFilter



class ExportActivityLogs(generics.ListAPIView):
    queryset = ActivityLog.objects.all().select_related("user")
    serializer_class = ExportActivityLogSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = LogsFilter

    def list(self, request, *args, **kwargs):
        filename = "user_logs"
        fields = [s.name for s in self.get_queryset().model._meta.fields]
        headers = [{"name": "%s" % (k.replace("_", " ").title()), "value": k} for k in fields]
        queryset = self.get_serializer(self.get_queryset(), many=True).data
        path = exportcsv(filename=filename, queryset=queryset, headers=headers, title="User Logs", export_csv=True,
                         request=self.request)
        return Response({"path": path})



