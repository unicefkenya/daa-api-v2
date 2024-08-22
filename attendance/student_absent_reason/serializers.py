from rest_framework import serializers

from school.models import StudentAbsentReason, Student
from school.student.serializers import StudentSerializer


class StudentAbsentReasonSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source="school.name", read_only=True)

    class Meta:
        model = StudentAbsentReason
        fields = "__all__"

        extra_kargs = {"unique_together": ("student", "date")}
