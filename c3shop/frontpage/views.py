from django.shortcuts import render
from django.http import HttpResponse
from .uitools.footerfunctions import render_footer
from .uitools.headerfunctions import render_header
from .uitools.body import *
from .management import edit_post, edit_user
from .uitools import ulog

# Create your views here.


def index(request):
    a = render_header(request)
    a += "<h1>index: Not yet implemented</h1>"
    a += render_article_list()
    a += render_footer(request)
    return HttpResponse(a)


def detailed_article(request, article_id):
    a = render_header(request)
    a += "<h1>article: Not yet implemented</h1>"
    a += render_article_detail(article_id)
    a += render_footer(request)
    return HttpResponse(a)


def detailed_post(request, post_id):
    a = render_header(request)
    a += render_post(post_id)
    a += render_footer(request)
    return HttpResponse(a)


def display_user(request, user_id):
    a = render_header(request)
    a += render_user_detail(user_id)
    a += render_footer(request)
    return HttpResponse(a)


def login(request):
    return ulog.login(request)


def admin_home(request):
    a = render_header(request)
    a += render_footer(request)
    return HttpResponse(a)


def admin_edit_post(request):

    response = require_login(request, min_required_user_rights=3)
    if response:
        return response
    a = render_header(request, admin=True)
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


def admin_add_user(request):
    response = require_login(request, min_required_user_rights=4)
    if response:
        return response
    a = render_header(request, admin=True)
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
    a = render_header(request, admin=True)
    a += render_user_list(request)
    a += render_footer(request)
    return HttpResponse(a)


def action_save_post(request):
    return edit_post.do_edit_action(request, "../../")


def action_save_user(request):
    return edit_user.do_edit_action(request, "../../")


def logout(request):
    return ulog.logout(request)
