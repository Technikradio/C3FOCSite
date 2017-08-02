from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^editpost/(?P<post_id>[0-9]+)$', views.admin_edit_post, name="post_edit"),
    url(r'^login/redirect-(?P<redirect>.+)$', views.admin_login, name="login"),
]