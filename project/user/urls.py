from django.conf.urls import url, include
from .views import *


urlpatterns = [
    url(r'^get_profile/$', user_get_profile),
    url(r'^get_profile/(?P<pk>[0-9]+)/$', user_get_profile_by_id),
    url(r'^update_profile/$', user_update_profile),
    url(r'^follow/(?P<pk>[0-9]+)/$', user_follow),
    url(r'^unfollow/(?P<pk>[0-9]+)/$', user_unfollow),
    url(r'following/$', user_following),
    url(r'following/(?P<pk>[0-9]+)/$', user_following_by_id),
    url(r'followers/$', user_followers),
    url(r'followers/(?P<pk>[0-9]+)/$', user_followers_by_id),
    # ...
]
