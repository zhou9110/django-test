from django.conf.urls import url
from rest_framework import routers
from project.appname.views import *

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'universities', UniversityViewSet)

urlpatterns = [
    url(r'customview', custom_view),
]

urlpatterns += router.urls
