#
#
#
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<medium_id>[0-9]+)$', views.detailed_media, name="media"),
]
