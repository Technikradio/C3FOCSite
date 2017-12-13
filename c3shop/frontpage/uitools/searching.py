from django.http import HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from ..management.form import Form, SearchBar, SubmitButton
from ..models import *


def render_search_bar(small: bool = True):
    f = Form()
    f.method = "get"
    f.action_url = "/search"
    f.add_content(SearchBar(name="search", do_cr_after_input=False))
    f.add_content(SubmitButton(do_cr_after_input=False))
    # TODO implement placeholder
    a = 'style="display: inline;" class="w3-bar-item w3-button'
    a += ' w3-hide-small w3-hover-white"'
    if not small:
        a = 'class="large_search_bar"'
    return '<span ' + a + '>' + f.render_html(None) + "</span>"  # Should be fine due to GET method


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
        try:
            for o in Article.objects.filter(description__contains=term):
                if (o not in results) and (o.quantity > 0 or include_sold_out_articles):
                    results.append(o)
        except ObjectDoesNotExist as e:
            pass  # It's not bad to drop this exception since no results simply means no data
        try:
            for o in Article.objects.filter(cachedText__contains=term):
                if (o not in results) and (o.quantity > 0 or include_sold_out_articles):
                    results.append(o)
        except ObjectDoesNotExist as e:
            pass
        try:
            for o in Article.objects.filter(size__contains=term):
                if (o not in results) and (o.quantity > 0 or include_sold_out_articles):
                    results.append(o)
        except ObjectDoesNotExist as e:
            pass
        try:
            for o in Post.objects.filter(title__contains=term):
                if o not in results:
                    results.append(o)
        except ObjectDoesNotExist as e:
            pass
        try:
            for o in Post.objects.filter(cacheText__contains=term):
                if o not in results:
                    results.append(o)
        except ObjectDoesNotExist as e:
            pass
        try:
            for o in Media.objects.filter(cachedText__contains=term):
                if o not in results:
                    results.append(o)
        except ObjectDoesNotExist as e:
            pass
        try:
            for o in Media.objects.filter(headline__contains=term):
                if o not in results:
                    results.append(o)
        except ObjectDoesNotExist as e:
            pass
    return results


def generate_preview(c: []):
    a = '<div class="search_preview">'
    for o in c:
        headline = ""
        body = ""
        link = ""
        if isinstance(o, Article):
            headline = o.description
            body = "Size: " + str(o.size) + " Pieces left: " + str(o.quantity) 
            body += "<br/>" + o.cachedText[:-50] + "..."
            link = "/article/" + str(o.pk)
        elif isinstance(o, Post):
            headline = str(o.title)
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
        a += '<div class="w3-text-teal w3-row w3-padding-64">No results matching query found.</div>'
    else: 
        a += generate_preview(results)
    return a
