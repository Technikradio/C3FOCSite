#
#
#
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.detailed_article, name="article"),
]