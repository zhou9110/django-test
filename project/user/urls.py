from django.conf.urls import url, include
from .views import *


urlpatterns = [
    url(r'^get_profile/$', user_get_profile),
    url(r'^edit_profile/$', user_edit_profile),
    url(r'^follow/$', user_follow),
    url(r'^unfollow/$', user_unfollow),
    url(r'get_following/$', user_get_following),
    url(r'get_followers/$', user_get_followers),
    # ...
]

