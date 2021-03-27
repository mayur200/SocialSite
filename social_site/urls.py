from django.urls import path
from . import views

#login = admin
#password = admin
app_name = 'social_site'

urlpatterns = [
    path('home/', views.home_view),
    path('detail/', views.tweet_detail_view,name='detail'),
    path('detail/<int:spirit_id>', views.tweet_detail_view, name='detail'),
    path('spirit/',views.tweet_list_view),
    path('cr_spirit/',views.spirit_create_view),
    path('home/api/spirit/action',views.tweet_action_view),
    path('api/spirit/<int:spirit_id>/delete',views.tweet_delete_view)
    ]
