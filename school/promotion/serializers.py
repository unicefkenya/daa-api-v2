from django.db.models import Subquery
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error

from mylib.my_common import MyCustomException
from school.promotion.models import PromoteStream, PromoteSchool


class PromoteStreamSerializer(serializers.ModelSerializer):
    next_class_name=serializers.CharField(source="next_class.class_name",read_only=True)
    class Meta:
        model=PromoteStream
        fields=('__all__')
        extra_kwargs={
            "promote_school":{
                "required":False,
            }
        }


class PromoteSchoolSerializer(serializers.ModelSerializer):
    stream_promotions=PromoteStreamSerializer(many=True)
    class Meta:
        model=PromoteSchool
        fields=('__all__')
        read_only_fields=('graduates_class',)
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=PromoteSchool.objects.all(),
                fields=('school', 'year'),
                message="Promotions already done for this school."
            )
        ]


    def create(self, validated_data):
        print(validated_data)
        stream_promotions=validated_data.pop("stream_promotions")
        promote_school=PromoteSchool.objects.create(**validated_data)
        streamproms=[]
        # print(stream_promotions)
        for streamprom in stream_promotions:
            p=PromoteStream(next_class=streamprom["next_class"],prev_class=streamprom["prev_class"],promote_school_id=promote_school.id)
            streamproms.append(p)
        PromoteStream.objects.bulk_create(streamproms)
        return promote_school
        # return promote_school

    def update(self, instance, validated_data):
        if instance.completed:raise MyCustomException("Promotion already completed. Undo to update.",404)
        stream_promotions = validated_data.pop("stream_promotions")
        stream_proms=PromoteStream.objects.filter(promote_school_id=instance.id)
        PromoteSchool.objects.filter(id=instance.id).update(**validated_data)
        for streamp in stream_promotions:
            PromoteStream.objects.filter(id__in= Subquery(stream_proms.values("id")) ).filter(prev_class=streamp["prev_class"]).update(**streamp)
        return instance

