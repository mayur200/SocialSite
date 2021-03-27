from django.contrib import admin
from .models import Tweet, TweetLike

# Register your models here.

class TweetLikeAdmin(admin.TabularInline):
    model = TweetLike

class SpiritAdmin(admin.ModelAdmin):
    inlines = [TweetLikeAdmin]
    list_display =  ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user_email'] #we cant search with username we have to use 'user__username' like user.username

    class Meta:
        model = Tweet


admin.site.register(Tweet, SpiritAdmin)

