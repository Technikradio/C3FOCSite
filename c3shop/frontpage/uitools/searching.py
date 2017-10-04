from django.http import HttpRequest
from ..management.form import Form, SearchBar
from ..models import *


def render_search_bar(small: bool = True):
    f = Form()
    f.method = "get"
    f.action_url = "/search"
    f.add_content(SearchBar(name="search"))
    # TODO implement placeholder
    a = "small_search_bar"
    if not small:
        a = "large_search_bar"
    return '<div class="' + a + '">' + f.render_html() + "</div>"


"""
Replace the __contains with __search as soon as you're using PostgreSQL since its search engine is far more efficient.
Also have a look on PostgreSQL search tuning.
"""


def perform_query(request: HttpRequest):
    term = ""
    results = []
    include_sold_out_articles = False
    if request.GET.get('search'):
        term = str(request.GET["search"])
    if request.GET.get('includeso'):
        include_sold_out_articles = bool(request.GET["includeso"])
    if term is not "":
        for o in Article.objects.get(description__contains=term):
            if (o not in results) and (o.quantity > 0 or include_sold_out_articles):
                results.append(o)
        for o in Article.objects.get(cachedText__contains=term):
            if (o not in results) and (o.quantity > 0 or include_sold_out_articles):
                results.append(o)
        for o in Article.objects.get(size__contains=term):
            if (o not in results) and (o.quantity > 0 or include_sold_out_articles):
                results.append(o)
        for o in Post.objects.get(title__contains=term):
            if o not in results:
                results.append(o)
        for o in Post.orbjects.get(cacheText__contains=term):
            if o not in results:
                results.append(o)
        for o in Media.objects.get(cachedText__contains=term):
            if o not in results:
                results.append(o)
        for o in Media.objects.get(headline__contains=term):
            if o not in results:
                results.append(o) 
    return results


def generate_preview(c: []):
    a = '<div class="search_preview">'
    for o in c:
        headline = ""
        body = ""
        link = ""
        if isinstance(o, Article):
            headline = o.description
            body = "Size: " + o.size + " Pieces left: " + o.quantity + "<br/>" + o.cachedText[:-50] + "..."
            link = "/article/" + str(o.pk)
        elif isinstance(o, Post):
            headline = o.title
            body = o.cacheText[:-50] + "..."
            link = "/post/" + str(o.pk)
        elif isinstance(o, Media):
            headline = o.headline
            body = o.cachedText
            link = "/medium/" + str(o.pk)
        a += '<a href="' + link + '"><article><h3>' + str(headline) + "</h2>" + body + "</article></a>"
    a += "</div>"
    return a


def render_result_page(request: HttpRequest):
    a = render_search_bar(small=False)
    results = perform_query(request)
    if len(results) < 1:
        a += "No results"
    else:
        for r in results:
            a += generate_preview(r)
    return a
