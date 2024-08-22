
from rest_framework import serializers
from support_question.models import SupportRequest
class SupportRequestSerializer(serializers.ModelSerializer):
    school_name=serializers.ReadOnlyField(source="school.name")
    school_emis_code=serializers.ReadOnlyField(source="school.emis_code")
    class Meta:
        model=SupportRequest
        fields=("__all__")
