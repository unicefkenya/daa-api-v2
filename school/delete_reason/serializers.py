from rest_framework import serializers

from school.models import DeleteReason, Student
from school.student.serializers import StudentSerializer


class DeleteReasonSerializer(serializers.ModelSerializer):
    school_name=serializers.CharField(source="school.name",read_only=True)
    class Meta:
        model=DeleteReason
        fields=("__all__")
