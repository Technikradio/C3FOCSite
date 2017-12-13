from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .uitools.footerfunctions import render_footer
from .uitools.headerfunctions import render_content_header
from .uitools.body import *
from .management import edit_post, edit_user, post_page, dashboard_page, reservation_page, reservation_actions, media_select
from .management import media_actions, media_upload_page, media_page, random_actions, article_actions, article_page
from .management import edit_article, edit_reservation, article_select, reservation_processing
from .uitools import ulog, searching

# Create your views here.


def index(request):
    a = render_content_header(request)
    a += render_index_page(request)
    a += render_article_list()
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


@csrf_exempt
def login(request):
    return ulog.login(request)


def admin_home(request):
    response = require_login(request)
    if response:
        return response
    return HttpResponse(dashboard_page.render_dashboard(request))


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


@csrf_exempt
def action_save_post(request):
    return edit_post.do_edit_action(request, "/admin/posts")


@csrf_exempt
def action_save_user(request):
    return edit_user.action_save_user(request, "/admin/users")


@csrf_exempt
def action_add_article_to_reservation(request: HttpRequest):
    return reservation_actions.add_article_action(request, "/admin/reservations")


@csrf_exempt
def action_alter_current_reservation(request: HttpRequest):
    return reservation_actions.manipulate_reservation_action(request, "/admin/reservations")


@csrf_exempt
def action_save_reservation(request: HttpRequest):
    return reservation_actions.write_db_reservation_action(request)


@csrf_exempt
def action_save_article(request: HttpRequest):
    response = require_login(request, min_required_user_rights=2)
    if response:
        return response
    return article_actions.action_save_article(request)


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
    a += render_footer()
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


@csrf_exempt
def action_add_single_media(request: HttpRequest):
    response = require_login(request, min_required_user_rights=0)
    if response:
        return response
    return media_actions.action_add_single_media(request)


@csrf_exempt
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

