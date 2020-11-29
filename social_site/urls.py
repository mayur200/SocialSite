from django.urls import path
from . import views


app_name = 'social_site'

urlpatterns = [
    path('home/', views.home_view),
    path('detail/', views.tweet_detail_view,name='detail'),
    path('detail/<int:spirit_id>', views.tweet_detail_view, name='detail'),
    path('spirit/',views.tweet_list_view),
    path('cr_spirit/',views.spirit_create_view),
    path('api/tweets/<int:spirit_id>/delete',views.tweet_delete_view)
    ]