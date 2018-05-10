from django.conf.urls import url, include
from .views import *


urlpatterns = [
    url(r'^posts/$', post_posts),
    url(r'^posts/(?P<uid>[0-9]+)/$', post_posts_by_uid),
    url(r'^post/(?P<pk>[0-9]+)/$', post_post),
    url(r'^create/$', post_create),
    url(r'^update/(?P<pk>[0-9]+)/$', post_update),
    url(r'^create_comment/(?P<pk>[0-9]+)/$', post_create_comment),
    url(r'^comments/(?P<pid>[0-9]+)/$', post_comments),
    url(r'^create_like/(?P<pk>[0-9]+)/$', post_create_like),
    url(r'^likes/(?P<pid>[0-9]+)/$', post_likes),
    url(r'^tag/(?P<pk>[0-9]+)/$', post_tag),
    url(r'^convert_tags/$', post_convert_tags),
    url(r'^create_tag/$', post_create_tag),
    url(r'^create_collection/$', post_create_collection),
    url(r'^collection/(?P<pk>[0-9]+)/$', post_collection),
    url(r'^collections/$', post_collections),
    url(r'^collections/(?P<uid>[0-9]+)/$', post_collections_by_uid),
    url(r'^update_collection/append/(?P<pk>[0-9]+)/$', post_update_collection_append),
    url(r'^update_collection/remove/(?P<pk>[0-9]+)/$', post_update_collection_remove),
    url(r'^update_collection/(?P<pk>[0-9]+)/$', post_update_collection),
    # ...
]
