from ..models import Article, Profile, Media, ArticleGroup
from ..uitools import body
from django.http import HttpRequest
from .magic import get_current_user, get_article_pcs_free
from .form import Form, PlainText, SubmitButton, NumberField, TextField, CheckBox, CheckEnum
from .dashboard_page import render_error_panel


def generate_edit_link(a: Article):
    return "/admin/articles/edit?article_id=" + str(a.pk)


def render_vs_status(b: bool):
    if b:
        return 'Visible'
    else:
        return '<img class="icon" src="/staticfiles/frontpage/error.png" alt="Invisible"/>'


def render_objects_form(request: HttpRequest):
    items_per_page = 50
    if request.GET.get('objects'):
        items_per_page = int(request.GET["objects"])
    name_filter = ""
    if request.GET.get('namefilter'):
        name_filter = str(request.GET["namefilter"])
    only_visible = False
    if request.GET.get("onlyvisible"):
        only_visible = True
    f: Form = Form(request.path)
    f.method = "get"
    f.add(PlainText("<h4>Filter:</h4><br />Objects per page: "))
    f.add(NumberField(name="objects", button_text=str(items_per_page)))
    f.add(PlainText("Description: "))
    f.add(TextField(name="namefilter", button_text=name_filter, required=False))
    f.add(CheckBox(text="Display only visible entries: ", name="onlyvisible", checked=CheckEnum.get_state(only_visible)))
    f.add(SubmitButton(button_text="Sort"))
    return f.render_html(request)


def render_group_list(request: HttpRequest, u: Profile):
    a = '<h4>Article groups:</h4>'
    if u.rights > 1:
        a += '<a href="' + request.path + '?msgid=notimplemented" class="button">Add Group</a><br />'

    prefilter = ArticleGroup.objects.all()
    if request.GET.get("namefilter"):
        prefilter = prefilter.filter(group_name=str(request.GET["namefilter"]))
    a += '<br /><table><tr>'
    if u.rights > 1:
        a += '<th> Edit </th><th> Group ID </th>'
    a += '<th> Article </th><th> Preview </th><th> Price </th></tr>'
    for g in prefilter:
        a += '<tr>'
        if u.rights > 1:
            a += '<td> Not yet Implemented </td><td>' + str(g.id) + '</td>'
        a += '<td>' + str(g.group_name) + '</td><td>' + body.render_image(g.group_flash_image, cssclass="icon")
        a += '</td><td> Not yet implemted </td></tr>'
    a += '</table>'
    return a


def render_alone_article_list(request: HttpRequest, u: Profile):
    # TODO add method to select how many posts to display
    # TODO make layout more fancy
    page = 1
    items_per_page = 50
    if request.GET.get('objects'):
        items_per_page = int(request.GET["objects"])
    prefilter = Article.objects.all().filter(group=None)
    if request.GET.get("namefilter"):
        prefilter = prefilter.filter(description=str(request.GET.get("namefilter")))
    if request.GET.get("onlyvisible"):
        prefilter = prefilter.filter(visible=True)
    total_items = prefilter.count()
    max_page = total_items / items_per_page
    if max_page < 1:
        max_page = 1
    if request.GET.get('page'):
        page = int(request.GET["page"])
    if page > max_page:
        page = max_page
    start_range = 1 + page * items_per_page
    if start_range > total_items:
        start_range = 0
    end_range = (page + 1) * items_per_page

    a = '<h4>Stand alone Articles:</h4>'
    if u.rights > 1:
        a += '<a href="/admin/articles/edit" class="button">Add a new Article</a><br/>'
    a += '<br /><table><tr>'
    if u.rights > 1:
        a += '<th>Edit</th>'
    a += '<th> Article ID </th><th> Preview </th><th> Description </th><th> Size </th>' \
         '<th> Price </th><th> Pcs left </th>'
    if u.rights > 1:
         a += '<th> Visibility </th>'
    a += '</tr>'
    objects = prefilter.filter(pk__range=(start_range, end_range))
    for article in objects:
        a += '<tr>'
        if u.rights > 1:
            a += '<td><a href="' + generate_edit_link(article) + '">' \
                '<img src="/staticfiles/frontpage/edit.png" class="button-img"/></a></td>'
        a += '<td>' + str(article.pk) + "</td><td>" + body.render_image(article.flashImage, cssclass="icon")\
                + "</td><td>" + article.description + "</td><td>"\
                + article.size + "</td><td>" + body.render_price(article.price) + "</td><td>"\
             + str(get_article_pcs_free(article)) + "</td>"
        if u.rights > 1:
            a += "<td>" + render_vs_status(article.visible) + "</td>"
        a += "</tr>"
    a += '</table><br />'
    if page > 1:
        a += '<a href="' + request.path + '?page=' + str(page - 1) + '&objects=' + str(items_per_page) \
                + '" class="button"> Previous page </a>'
    if page < max_page:
        a += '<a href="' + request.path + '?page=' + str(page + 1) + '&objects=' + str(items_per_page) \
                + '" class="button"> Next page </a>'
    a += '<center>displaying page ' + str(page) + ' of ' + str(max_page) + ' total pages.</center>'
    return a


def render_article_page(request: HttpRequest):
    forcefilter: bool = False
    if request.GET.get("showfilter"):
        forcefilter = True
    u: Profile = get_current_user(request)
    a = render_error_panel(request)
    a += '<div class="admin-popup w3-row w3-padding-64 w3-twothird w3-container"><h3>Articles:</h3><br/>'
    if u.rights > 1 or forcefilter:
        a += render_objects_form(request)
    a += render_group_list(request, u)
    a += render_alone_article_list(request, u)
    if u.rights > 1 or forcefilter:
        a += render_objects_form(request)
    a += '</div>'
    return a

