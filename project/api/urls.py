from django.conf.urls import url
from rest_framework import routers
from .views import *


urlpatterns = [
    url(r'customview', custom_view),
]
