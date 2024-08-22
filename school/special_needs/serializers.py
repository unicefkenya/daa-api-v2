
from rest_framework import serializers
from school.models import SpecialNeed
class SpecialNeedSerializer(serializers.ModelSerializer):
    class Meta:
        model=SpecialNeed
        fields=("__all__")
