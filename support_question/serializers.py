from rest_framework import serializers

from support_question.models import SupportQuestion


class SupportQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=SupportQuestion
        fields=("__all__")
