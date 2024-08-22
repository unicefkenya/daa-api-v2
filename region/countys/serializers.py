
from rest_framework import serializers
from region.models import County
from region.sub_countys.serializers import SubCountySerializer


class CountySerializer(serializers.ModelSerializer):
    sub_counties=SubCountySerializer(many=True,read_only=True)
    class Meta:
        model=County
        fields=("__all__")
