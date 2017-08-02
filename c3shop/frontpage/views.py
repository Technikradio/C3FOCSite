from django.shortcuts import render
from django.http import HttpResponse
from .uitools.footerfunctions import render_footer
from .uitools.headerfunctions import render_header
from .uitools.body import render_article_list, render_article_detail, render_post, render_user_detail, require_login

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


def admin_login(request, redirect):
    pass


def admin_edit_post(request, post_id):
    response = require_login(request, min_required_user_rights=1)
    if response:
        return response
    pass

