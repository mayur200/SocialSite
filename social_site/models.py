from django.db import models
import random
from django.conf import settings

User = settings.AUTH_USER_MODEL

#user = admin
#email = admin@gmail.com
#password = admin
# Create your models here.

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spirit = models.ForeignKey("Tweet", on_delete=models.CASCADE) #Tweet = Class Name
    timestamp = models.DateTimeField(auto_now_add=True)


class Tweet(models.Model):
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='spirit_user', blank=True, through=TweetLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='image/',blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 12),
        }
