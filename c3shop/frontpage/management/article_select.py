from django.http import HttpRequest
from django.http import HttpResponse
from ..models import Article
from .page_skeleton import render_headbar, render_footer


def render_article_selection_page(request: HttpRequest):
    page = 1
    if request.GET.get('page'):
        page = int(request.GET['page'])
    items_per_page = 50
    if request.GET.get('objects'):
        items_per_page = int(request.GET["objects"])
    total_items = Article.objects.all().count()
    max_page = total_items / items_per_page
    if max_page < 1:
        max_page = 1
    if page > max_page:
        page = max_page
    start_range = 1 + page * items_per_page
    if start_range > total_items:
        start_range = 0
    end_range = (page + 1) * items_per_page
    a = render_headbar(request, title="Select media")
    a += '<div class="admin-popup">'
    a += '<h3>Please select your desired article</h3><table><tr><th>Select</th><th>Preview</th><th>Title</th></tr>'
    objects = Article.objects.filter(pk__range=(start_range, end_range))
    for article in objects:
        s: str = ""
        p = article.flashImage
        if p:
            s = p.lowResFile
        else:
            s = "/staticfiles/frontpage/no-image.png"
        a += '<tr><td><a href="/admin/reservations/article-detail-select?article_id=' + str(article.pk)
        a += '"><img src="/staticfiles/frontpage/order-article.png" class="button"/></a></td><td><img src="'
        a += s + '" /></td><td>' + article.description + '</td></tr>'
    a += '</table>'
    if page > 1:
        a += '<a href="' + request.path + '?page=' + str(page - 1) + '&objects=' + str(objects) + \
             '" class="button">Previous page </a>'
    if page < max_page:
        a += '<a href="' + request.path + '?page=' + str(page + 1) + '&objects=' + str(objects) + \
             '" class="button">Next page </a>'
    a += '</div>' + render_footer(request)
    return HttpResponse(a)
