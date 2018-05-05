from django.conf.urls import url, include
from django.contrib import admin
admin.autodiscover()

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
    url(r'login', user_login),
    url(r'register', user_register),
    url(r'change_password', user_change_password),
    url(r'logout', user_logout),
    # ...
]
