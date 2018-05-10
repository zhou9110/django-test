from django.conf.urls import url, include
from .views import *


urlpatterns = [
    url(r'^posts/$', post_posts),
    url(r'^posts/(?P<uid>[0-9]+)/$', post_posts_by_uid),
    url(r'^post/(?P<pk>[0-9]+)/$', post_post),
    url(r'^create/$', post_create),
    url(r'^update/(?P<pk>[0-9]+)/$', post_update),
    url(r'^comment/(?P<pk>[0-9]+)/$', post_comment),
    url(r'^like/(?P<pk>[0-9]+)/$', post_like),
    url(r'^tag/(?P<pk>[0-9]+)/$', post_tag),
    url(r'^create_tag/$', post_create_tag),
    # ...
]
