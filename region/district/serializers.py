from rest_framework import serializers

from region.models import District


class DistrictSerializer(serializers.ModelSerializer):
    region_name=serializers.CharField(source="region.name",read_only=True)
    class Meta:
        model=District
        fields=("__all__")