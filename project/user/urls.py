from django.conf.urls import url, include
from .views import *


urlpatterns = [
    url(r'^get_profile/$', get_profile),
    url(r'^edit_profile/$', edit_profile),
    # ...
]

