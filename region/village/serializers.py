from rest_framework import serializers

from region.models import Village


class VillageSerializer(serializers.ModelSerializer):
    district_name=serializers.CharField(source="district.name",read_only=True)
    region_name=serializers.CharField(source="district.region.name",read_only=True)
    class Meta:
        model=Village
        fields=("__all__")