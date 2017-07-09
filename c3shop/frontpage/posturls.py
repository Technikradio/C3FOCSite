#
#
#
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<post_id>[0-9]+)$', views.detailed_post, name="post"),
]
