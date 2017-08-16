from .models import Answers
from rest_framework import serializers


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ('question', 'answer')