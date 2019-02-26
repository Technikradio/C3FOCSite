#
#
#
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<article_id>[0-9]+)$', views.detailed_article, name="article"),
]
