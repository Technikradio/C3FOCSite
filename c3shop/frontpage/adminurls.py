from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^editpost/(?P<post_id>[0-9]+)$', views.admin_edit_post, name="post_edit"),
    url(r'^users', views.admin_list_users, name="list_users"),
    url(r'^users/', views.admin_list_users, name="list_users"),
    url(r'^users/add', views.admin_add_user, name="add_user"),

]