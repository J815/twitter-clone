"""twitting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path, re_path, include
from tweets.views import home_view,tweet_detail_view, tweets_list_view , tweet_create_view, delete_view, action_view
from django.views.generic import TemplateView
from account.views import login_view, logout_view, signup_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('signup/', signup_view),
    path('<int:id>',tweet_detail_view),
    path('tweet/',tweets_list_view),
    path('create',tweet_create_view),
    re_path(r'profiles?/', include('profiles.urls')),
    re_path(r'api/profiles?/', include('profiles.api.urls')),
    path('api/twe/', include('tweets.urls'))
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                  document_root=settings.STATIC_ROOT)