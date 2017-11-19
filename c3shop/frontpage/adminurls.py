from django.conf.urls import url
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
    url(r'^actions/add-article-to-reservation', views.action_add_article_to_reservation,
        name="action_add_to_reservation"),
    url(r'^actions/alter-current-reservation', views.action_alter_current_reservation, name="action_alter_reservation"),
    url(r'^actions/save-current-reservation', views.action_save_reservation, name="action_save_reservation"),
    url(r'^actions/add-single-media', views.action_add_single_media, name="action_single_media_add"),
    url(r'^actions/add-bulk-media', views.action_add_bulk_media, name="action_bulk_media_add"),
    url(r'^actions/change-user-avatar', views.action_change_avatar, name="action_change_avatar"),
    url(r'^actions/change-open-status', views.action_change_open_status, name="action_change_open_status"),
    url(r'^actions/save-article', views.action_save_article, name="action_save_article"),
    url(r'^actions/change-article-splash-image', views.admin_select_article_flash_image,
        name="action_change_article_flash_image"),
    url(r'^actions/delete-post', views.admin_delete_post_action, name="action_delete_post"),
    url(r'^actions/add-image-to-article', views.admin_add_media_to_article_action, name="add_img_to_article"),
    url(r'^articles/edit', views.admin_edit_article, name="article_edit"),
    url(r'^articles$', views.admin_show_articles, name="list_articles"),
    url(r'^media/select', views.admin_select_media, name="wizard_select_media"),
    url(r'^media/add', views.admin_add_media, name="add_media"),
    url(r'^media$', views.admin_show_media, name="media_page"),
    url(r'^reservations$', views.admin_display_orders, name="list_orders"),
    url(r'^reservations/$', views.admin_display_orders, name="list_orders"),
    url(r'^reservations/edit', views.admin_edit_reservation, name='edit_reservation'),
    url(r'^reservations/select-article', views.admin_select_article, name="wizard_select_article"),
    url(r'^reservations/article-detail-select', views.admin_select_article_detail, name="wizard_select_article_p2"),
    url(r'^reservations/process', views.admin_process_reservation, name="wizard_process_reservation"),
    url(r'^confirm', views.admin_confirm_action, name="admin_confirm"),
]
