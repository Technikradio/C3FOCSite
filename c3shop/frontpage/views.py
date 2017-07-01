from django.shortcuts import render
from django.http import HttpResponse
from .uitools.footerfunctions import render_footer
from .uitools.headerfunctions import render_header
from .uitools.body import render_article_list

# Create your views here.


def index(request):
    a = render_header(request)
    a += "<h1>index: Not yet implemented</h1>"
    a += render_article_list()
    a += render_footer(request)
    return HttpResponse(a)


def detailed_article(resquest):
    a = render_header(request)
    a += "<h1>article: Not yet implemented</h1>"
    a += render_footer(request)
    return HttpResponse(a)

