from django.urls import path
from .views import home_view,tweet_feed_view,  details_view,tweet_list_view , tweet_create_view, delete_view, action_view

urlpatterns = [
    
    path('', tweet_list_view),
    path('feed/', tweet_feed_view),
    path('<int:tweet>/',details_view),
    path('create',tweet_create_view),
    path('action',action_view),
    path('<int:tweet>/delete', delete_view)
    
]