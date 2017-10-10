from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.admin_dashboard, name="dashboard"),
    url(r'^posts$', views.admin_list_posts, name='list_posts'),
    url(r'^posts/$', views.admin_list_posts, name='list_posts'),
    url(r'^posts/edit', views.admin_edit_post, name="post_edit"),
    url(r'^users$', views.admin_list_users, name="list_users"),
    url(r'^users/$', views.admin_list_users, name="list_users"),
    url(r'^users/edit', views.admin_edit_user, name="user_edit"),
    url(r'^actions/save-post', views.action_save_post, name="action_save_post"),
    url(r'^actions/save-user', views.action_save_user, name="action_save_post"),
    url(r'^orders$', views.admin_display_orders, name="list_orders"),
    url(r'^orders/$', views.admin_display_orders, name="list_orders"),
]
