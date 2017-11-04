from ..models import Article, Profile
from django.http import HttpRequest
from .magic import get_current_user


def generate_edit_link(a: Article):
    return "/admin/articles/edit?article_id=" + str(a.pk)


def render_article_list(request: HttpRequest):
    # TODO add method to select how many posts to display
    # TODO make layout more fancy
    page = 1
    items_per_page = 50
    if request.GET.get('objects'):
        items_per_page = int(request.GET["objects"])
    total_items = Article.objects.all().count()
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

    a = '<div class="admin-popup">'
    a += '<h3>Articles:</h3><a href="/admin/articles/edit" class="button">Add a new Article</a><br/>' \
         '<br /><table><tr><th>Edit</th><th> Article ID </th><th> Description </th><th> Size </th>' \
         '<th> Price </th><th> Visibility </th></tr>'
    objects = Article.objects.filter(pk__range=(start_range, end_range))
    for article in objects:
        a += '<tr><td><a class="button" href="' + generate_edit_link(article) + '">' \
                '<img src="/staticfiles/frontpage/edit.png"/></a></td><td>' + str(article.pk) + "</td><td>" + \
             article.description + "</td><td>" + article.size + "</td><td>" + article.price + "</td><td>"\
             + str(article.visible) + "</td></tr>"
    a += '</table>'
    if page > 1:
        a += '<a href="' + request.path + '?page=' + str(page - 1) + '&objects=' + str(objects) + '" class="button">' \
                                                                                                  'Previous page </a>'
    if page < max_page:
        a += '<a href="' + request.path + '?page=' + str(page + 1) + '&objects=' + str(objects) + '" class="button">' \
                                                                                                  'Next page </a>'
    a += '<center>displaying page ' + str(page) + ' of ' + str(max_page) + ' total pages.</center>'
    a += '</div>'
    return a


def render_article_page(request: HttpRequest):
    u: Profile = get_current_user(request)
    a = '<h3>Articles</h3><br/>'
    a += render_article_list(request)
    return a

