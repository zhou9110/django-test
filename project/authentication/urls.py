from django.conf.urls import url, include
from rest_framework import routers
from .views import *


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^login/$', auth_login),
    url(r'^register/$', auth_register),
    url(r'^update_password/$', auth_update_password),
    url(r'^logout/$', auth_logout),
    # ...
]
