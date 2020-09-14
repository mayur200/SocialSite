from django.urls import path
from .  import views


app_name = 'social_site'

urlpatterns = [
    path('home/', views.home_view),
    path('detail/<int:tweet_id>', views.tweet_detail_view),
    path('tweets/',views.tweet_list_view)
    ]