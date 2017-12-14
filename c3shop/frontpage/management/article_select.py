
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from ..models import Article
from .page_skeleton import render_headbar, render_footer
from .form import Form, NumberField, TextArea, SubmitButton, PlainText
from .magic import get_article_pcs_free


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
    a = render_headbar(request, title="Select article")
    a += '<div class="w3-row w3-padding-64 w3-twothird w3-container">'
    a += '<h3>Please select your desired article</h3><table><tr><th>Select</th><th>Preview</th><th>Title</th></tr>'
    objects = Article.objects.filter(pk__range=(start_range, end_range))
    for article in objects:
        s: str = None
        p = article.flashImage
        if p:
            s = p.lowResFile
        else:
            s = "/staticfiles/frontpage/no-image.png"
        a += '<tr><td><a href="/admin/reservations/article-detail-select?article_id=' + str(article.pk)
        a += '"><img src="/staticfiles/frontpage/order-article.png" class="button-img"/></a></td><td><img src="'
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


def render_detail_selection(request: HttpRequest):
    try:
        a: Article = Article.objects.get(pk=int(request.GET["article_id"]))
        f: Form = Form()
        f.action_url = "/admin/actions/add-article-to-reservation?article_id=" + str(a.pk) + \
                       "&redirect=/admin/reservations/edit"
        f.add_content(PlainText("Specify amount: "))
        f.add_content(NumberField(name="quantity", minimum=1, maximum=get_article_pcs_free(a)))
        # TODO change to total available amount
        f.add_content(PlainText("Maybe add some optional notes:"))
        f.add_content(TextArea(name="notes", label_text="Notes:", text=""))
        f.add_content(SubmitButton())
        a = render_headbar(request, title="Specify article details")
        a += '<div class=""><div class="w3-row w3-padding-64 w3-twothird w3-container"><h3>Please specify further details:</h3>'
        a += f.render_html(request)
        a += '</div></div>' + render_footer(request)
        return HttpResponse(a)
    except Exception as e:
        return redirect("/admin/?error=" + str(e))
