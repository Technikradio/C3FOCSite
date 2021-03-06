from django.http import HttpResponse, HttpResponseForbidden

from frontpage.management.export import export_dbhints, export_statistics, export_invoice
from .uitools.footerfunctions import render_footer
from .uitools.headerfunctions import render_content_header
from .uitools.body import *
from .management import edit_post, edit_user, post_page, dashboard_page, reservation_page, reservation_actions
from .management import random_actions
from frontpage.management.mediatools import media_page, media_upload_page, media_actions, media_select
from .management import edit_reservation, reservation_processing, settings_page
from frontpage.management.articletools import article_select, article_actions, article_page, edit_article
from .management import edit_settings, password_page
from frontpage.management.grouptools import edit_group

from .management.grouptools.grouparticlesupdate import handle_group_articles_request
from frontpage.management.grouptools.grouparticlesadd import handle_group_article_add
from frontpage.management.grouptools.grouparticlesrelease import handle_release_group_request
from frontpage.management.grouptools.groupmetaupdate import handle_group_metadata_update
from .uitools import ulog, searching

# Create your views here.


def index(request):
    a = render_content_header(request)
    a += render_index_page(request)
    a += render_footer(request)
    return HttpResponse(a)


def detailed_article(request, article_id):
    a = render_content_header(request)
    a += render_article_detail(article_id)
    a += render_footer(request)
    return HttpResponse(a)


def detailed_post(request, post_id):
    a = render_content_header(request)
    a += render_post(post_id, request)
    a += render_footer(request)
    return HttpResponse(a)


def display_user(request, user_id):
    a = render_content_header(request)
    a += render_user_detail(user_id)
    a += render_footer(request)
    return HttpResponse(a)


def login(request):
    return ulog.login(request)


def admin_home(request):
    response = require_login(request)
    if response:
        return response
    return HttpResponse(dashboard_page.render_dashboard(request))


def admin_password_page(request: HttpRequest):
    response= require_login(request)
    if response:
        return response
    a = render_content_header(request, admin_popup=True)
    a += password_page.render_password_change_panel(request)
    a += render_footer(request)
    return HttpResponse(a)


def admin_edit_post(request):

    response = require_login(request, min_required_user_rights=3)
    if response:
        return response
    a = render_content_header(request, admin_popup=True, title="Edit post")
    post_id_string = ""
    if request.GET.get("post_id"):
        post_id_string = 'post_id=' + str(request.GET["post_id"]) + ''
    redirect_string = ""
    if post_id_string != "":
        redirect_string += "&"
    redirect_string += 'redirect=' + str(request.path) + ''
    a += edit_post.render_edit_page(request, '/admin/actions/save-post?' + post_id_string + redirect_string)
    a += render_footer(request)
    return HttpResponse(a)


def admin_list_posts(request):
    response = require_login(request)
    if response:
        return response
    a = render_content_header(request, admin_popup=True)
    a += post_page.render_post_list(request)
    a += render_footer(request)
    return HttpResponse(a)


def admin_edit_user(request):
    response = require_login(request, min_required_user_rights=4)
    if response:
        return response
    a = render_content_header(request, admin_popup=True)
    user_id_string = ""
    if request.GET.get("user_id"):
        user_id_string = 'user_id=' + str(request.GET["user_id"]) + ''
    redirect_string = ""
    if user_id_string != "":
        redirect_string += "&"
    redirect_string += 'redirect=' + request.path + ''
    a += edit_user.render_edit_page(request, '/admin/actions/save-user?' + user_id_string + redirect_string)
    a += render_footer(request)
    return HttpResponse(a)


def admin_edit_article(request: HttpRequest):
    response = require_login(request, min_required_user_rights=3)
    if response:
        return response
    a = render_content_header(request, admin_popup=True)
    a += edit_article.render_edit_page(request)
    a += render_footer(request)
    return HttpResponse(a)


def admin_list_users(request):
    response = require_login(request, min_required_user_rights=1)
    if response:
        return response
    a = render_content_header(request, admin_popup=True)
    a += render_user_list(request)
    a += render_footer(request)
    return HttpResponse(a)


def action_save_post(request):
    return edit_post.do_edit_action(request, "/admin/posts")


def action_change_password(request: HttpRequest):
    response = require_login(request, min_required_user_rights=0)
    if response:
        return response
    return password_page.action_change_password(request)


def action_save_user(request):
    return edit_user.action_save_user(request, "/admin/users")


def admin_delete_article_from_pending_reservation(request: HttpRequest):
    response = require_login(request, min_required_user_rights=0)
    if response:
        return response
    return reservation_actions.action_delete_article(request)


def action_add_article_to_reservation(request: HttpRequest):
    return reservation_actions.add_article_action(request, "/admin/reservations")


def action_alter_current_reservation(request: HttpRequest):
    return reservation_actions.manipulate_reservation_action(request, "/admin/reservations")


def action_save_reservation(request: HttpRequest):
    return reservation_actions.write_db_reservation_action(request)


def action_save_article(request: HttpRequest):
    response = require_login(request, min_required_user_rights=2)
    if response:
        return response
    return article_actions.action_save_article(request)


def action_update_group_articles(request: HttpRequest):
    response = require_login(request, min_required_user_rights=4)
    if response:
        return response
    return handle_group_articles_request(request)


def action_add_article_to_group(request: HttpRequest):
    response = require_login(request, min_required_user_rights=4)
    if response:
        return response
    return handle_group_article_add(request)


def action_alter_group_metadata(request: HttpRequest):
    response = require_login(request, min_required_user_rights=4)
    if response:
        return response
    return handle_group_metadata_update(request)


def action_release_group(request: HttpRequest):
    response = require_login(request, min_required_user_rights=4)
    if response:
        return response
    return handle_release_group_request(request)


def admin_export(request: HttpRequest):
    response = require_login(request, min_required_user_rights=0)
    if response:
        return response
    if request.GET["method"] == "userpdf":
        return export_invoice.export_user_invoice(request, int(request.GET["reservation"]))
    response = require_login(request, min_required_user_rights=2)
    if response:
        return response
    if request.GET.get("method"):
        if request.GET["method"] == "pdf":
            return export_invoice.export_orders_to_pdf(request, request.GET["reservations"].split(','))
        if request.GET["method"] == "rejectstatistics":
            return export_statistics.export_reject_statistics(request)
        if request.GET["method"] == "datadump":
            return export_dbhints.request_data_dump(request)
    return HttpResponseForbidden()


def admin_edit_group(request: HttpRequest):
    response = require_login(request, min_required_user_rights=4)
    if response:
        return response
    a = render_content_header(request, admin_popup=True)
    a += edit_group.render_edit_page(request)
    a += render_footer(response)
    return HttpResponse(a)


def logout(request):
    return ulog.logout(request)


def search(request: HttpRequest):
    a = render_content_header(request)
    a += searching.render_result_page(request)
    a += render_footer(request)
    return HttpResponse(a)


def detailed_media(request: HttpRequest, medium_id):
    a = render_content_header(request)
    a += render_image_detail(request, medium_id)
    a += render_footer(request)
    return HttpResponse(a)


def admin_display_orders(request: HttpRequest):
    response = require_login(request, min_required_user_rights=1)
    if response:
        return response
    a = render_content_header(request, admin_popup=True)
    a += reservation_page.render_order_page(request)
    a += render_footer(request)
    return HttpResponse(a)


def action_change_avatar(request: HttpRequest):
    response = require_login(request)
    if response:
        return response
    return media_actions.action_change_user_avatar(request)


def admin_dashboard(request: HttpRequest):
    response = require_login(request)
    if response:
        return response
    return HttpResponse(dashboard_page.render_dashboard(request))


def admin_select_media(request: HttpRequest):
    response = require_login(request)
    if response:
        return response
    return media_select.render_media_selection_page(request)


def handler404(request: HttpRequest):
    a = render_content_header(request)
    a += render_404_page(request)
    a += render_footer(request)
    response: HttpResponse = HttpResponse(a)
    response.status_code = 404
    return response


def admin_add_media(request: HttpRequest):
    response = require_login(request, min_required_user_rights=1)
    if response:
        return response
    a = render_content_header(request, admin_popup=True)
    a += media_upload_page.render_upload_page(request)
    a += render_footer(request)
    return HttpResponse(a)


def action_add_single_media(request: HttpRequest):
    response = require_login(request, min_required_user_rights=0)
    if response:
        return response
    return media_actions.action_add_single_media(request)


def action_add_bulk_media(request: HttpRequest):
    response = require_login(request, min_required_user_rights=1)
    if response:
        return response
    return media_actions.action_add_multiple_media(request)


def action_change_open_status(request: HttpRequest):
    response = require_login(request, min_required_user_rights=2)
    if response:
        return response
    return random_actions.action_change_store_open_status(request)


def admin_show_media(request: HttpRequest):
    response = require_login(request, min_required_user_rights=0)
    if response:
        return response
    a = render_content_header(request, admin_popup=True)
    a += media_page.render_media_page(request)
    a += render_footer(request)
    return HttpResponse(a)


def admin_show_articles(request: HttpRequest):
    response = require_login(request, min_required_user_rights=0)
    if response:
        return response
    a = render_content_header(request, admin_popup=True)
    a += article_page.render_article_page(request)
    a += render_footer(request)
    return HttpResponse(a)


def admin_edit_reservation(request: HttpRequest):
    response = require_login(request)
    if response:
        return response
    a = render_content_header(request, admin_popup=True)
    a += edit_reservation.render_edit_page(request)
    a += render_footer(request)
    return HttpResponse(a)


def admin_confirm_action(request: HttpRequest):
    response = require_login(request, min_required_user_rights=0)
    if response:
        return response
    a = render_content_header(request, admin_popup=True)
    a += random_actions.render_confirm_popup(request)
    a += render_footer(request)
    return HttpResponse(a)


def admin_select_article(request: HttpRequest):
    response = require_login(request)
    if response:
        return response
    return article_select.render_article_selection_page(request)


def admin_select_article_detail(request: HttpRequest):
    response = require_login(request)
    if response:
        return response
    return article_select.render_detail_selection(request)


def admin_select_article_flash_image(request: HttpRequest):
    response = require_login(request)
    if response:
        return response
    return article_actions.action_change_splash_image(request)


def admin_delete_post_action(request: HttpRequest):
    response = require_login(request, min_required_user_rights=4)
    if response:
        return response
    return edit_post.do_delete_action(request)


def admin_add_media_to_article_action(request: HttpRequest):
    response = require_login(request, min_required_user_rights=2)
    if response:
        return HttpResponseForbidden()
    return article_actions.action_add_media_to_article(request)


def admin_process_reservation(request: HttpRequest):
    response = require_login(request, min_required_user_rights=1)
    if response:
        return response
    a = render_content_header(request, admin_popup=True)
    a += reservation_processing.render_process_wizard(request)
    a += render_footer(request)
    return HttpResponse(a)


def action_finish_reservation_processing(request: HttpRequest):
    response = require_login(request, min_required_user_rights=1)
    if response:
        return HttpResponseForbidden()
    return reservation_processing.action_finish_reservation_processing(request)


def action_close_reservation(request: HttpRequest):
    response = require_login(request, min_required_user_rights=1)
    if response:
        return HttpResponseForbidden()
    return reservation_processing.action_close_reservation(request)


def action_quick_quantity_decrease(request: HttpRequest):
    response = require_login(request, min_required_user_rights=1)
    if response:
        return HttpResponseForbidden()
    return article_actions.action_quick_quantity_decrease(request)


def admin_settings_page(request: HttpRequest):
    response = require_login(request, min_required_user_rights=4)
    if response:
        return response
    a = render_content_header(request, admin_popup=True)
    a += settings_page.render_settings_page(request)
    a += render_footer(request)
    return HttpResponse(a)


def admin_settings_header(request: HttpRequest):
    response = require_login(request, min_required_user_rights=4)
    if response:
        return response
    a = render_content_header(request, admin_popup=True)
    a += edit_settings.render_header_edit_panel(request)
    a += render_footer(request)
    return HttpResponse(a)


def action_save_header_setting(request: HttpRequest):
    response = require_login(request, min_required_user_rights=4)
    if response:
        return HttpResponseForbidden()
    return random_actions.action_set_header_content(request)


def action_save_footer_setting(request: HttpRequest):
    response = require_login(request, min_required_user_rights=4)
    if response:
        return HttpResponseForbidden()
    return random_actions.action_set_footer_content(request)


def admin_settings_footer(request: HttpRequest):
    response = require_login(request, min_required_user_rights=4)
    if response:
        return response
    a = render_content_header(request, admin_popup=True)
    a += edit_settings.render_footer_edit_panel(request)
    a += render_footer(request)
    return HttpResponse(a)

