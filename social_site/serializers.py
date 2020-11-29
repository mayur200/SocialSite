from rest_framework import  serializers
from django.conf import settings
from .models import Tweet



class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ['content']


    def validate_content(self, value):
        if len(value) > settings.MAX_SPIRIT_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value
