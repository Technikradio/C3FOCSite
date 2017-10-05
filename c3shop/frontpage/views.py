from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .uitools.footerfunctions import render_footer
from .uitools.headerfunctions import render_content_header
from .uitools.body import *
from .management import edit_post, edit_user, post_page, dashboard_page, order_page
from .uitools import ulog, searching

# Create your views here.


def index(request):
    a = render_content_header(request)
    a += "<h1>index: Not yet implemented</h1>"
    a += render_article_list()
    a += render_footer(request)
    return HttpResponse(a)


def detailed_article(request, article_id):
    a = render_content_header(request)
    a += "<h1>article: Not yet implemented</h1>"
    a += render_article_detail(article_id)
    a += render_footer(request)
    return HttpResponse(a)


def detailed_post(request, post_id):
    a = render_content_header(request)
    a += render_post(post_id)
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
        post_id_string = 'post_id="' + str(request.GET["post_id"]) + '"'
    redirect_string = ""
    if post_id_string != "":
        redirect_string += "+"
    redirect_string += 'redirect="' + request.path + '"'
    edit_post.render_edit_page(request, '/admin/actions/save-post?' + post_id_string + redirect_string)
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
        user_id_string = 'user_id="' + str(request.GET["user_id"]) + '"'
    redirect_string = ""
    if user_id_string != "":
        redirect_string += "+"
    redirect_string += 'redirect="' + request.path + '"'
    edit_user.render_edit_page(request, '/admin/actions/save-post?' + user_id_string + redirect_string)
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
    return edit_post.do_edit_action(request, "../../")


def action_save_user(request):
    return edit_user.do_edit_action(request, "../../")


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
    a += order_page.render_order_page()
    a += render_footer(request)
    return HttpResponse(a)


def admin_dashboard(request: HttpRequest):
    response = require_login(request)
    if response:
        return response
    return HttpResponse(dashboard_page.render_dashboard(request))


def handler404(request: HttpRequest):
    a = render_content_header(request)
    a += render_404_page(request)
    a += render_footer()
    response: HttpResponse = HttpResponse(a)
    response.status_code = 404
    return response