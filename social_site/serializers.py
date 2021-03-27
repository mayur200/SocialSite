from rest_framework import  serializers
from django.conf import settings
from .models import Tweet


class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self,value):
        value = value.lower().strip() #'Like' -> 'like'
        if not value in settings.TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not validate action for serializer")
        return  value


class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.Serializer
    class Meta:
        model = Tweet
        fields = ['id','content','likes']
    def get_likes(self, obj):
        return obj.likes.count()


    def validate_content(self, value):
        if len(value) > settings.MAX_SPIRIT_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value
