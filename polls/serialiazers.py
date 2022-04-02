from rest_framework import serializers
from polls.models import Question


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_txt', 'pub_date']