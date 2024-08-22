from rest_framework import serializers


class BaseTeacherAttendanceDynamicStatsSerializer(serializers.Serializer):
    attendances = serializers.ReadOnlyField()
    present = serializers.ReadOnlyField()
    absent = serializers.ReadOnlyField()