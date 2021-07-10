from django.urls import path
from . import views

#login = admin
#password = admin
app_name = 'social_site'

urlpatterns = [
    path('', views.home_view),
    path('<int:spirit_id>/', views.tweet_detail_view, name='detail'),
    path('spirit/',views.tweet_list_view),
    path('cr_spirit/',views.spirit_create_view),
    path('action/',views.tweet_action_view),
    path('<int:spirit_id>/delete/',views.tweet_delete_view)
    ]
