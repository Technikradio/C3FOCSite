#
#
#
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^display/(?P<user_id>[0-9]+)$', views.display_user, name="display_user"),
]
