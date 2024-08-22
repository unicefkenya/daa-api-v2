from rest_framework import serializers

from school.models import AbsentReason, Student
from school.student.serializers import StudentSerializer


class AbsentReasonSerializer(serializers.ModelSerializer):
    school_name=serializers.CharField(source="school.name",read_only=True)
    class Meta:
        model=AbsentReason
        fields=("__all__")
