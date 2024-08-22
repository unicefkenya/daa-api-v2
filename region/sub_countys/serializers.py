
from rest_framework import serializers
from region.models import SubCounty
class SubCountySerializer(serializers.ModelSerializer):
    class Meta:
        model=SubCounty
        fields=("__all__")
