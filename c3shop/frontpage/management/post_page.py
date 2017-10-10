from django.http import HttpRequest
from ..models import Post


def generate_edit_link(p: Post):
    return "/admin/posts/edit?post_id=" + str(p.pk)


def render_post_list(request: HttpRequest):
    # TODO add method to select how many posts to display
    # TODO make layout more fancy
    page = 1
    items_per_page = 50
    total_items = Post.objects.all().count()  # This method isn't totally super dumb since django query sets are lazy.
    max_page = total_items / items_per_page
    if request.GET.get('page'):
        page = int(request.GET["page"])
    if request.GET.get('objects'):
        items_per_page = int(request.GET["objects"])
    if page > max_page:
        page = max_page
    start_range = 1 + page * items_per_page
    end_range = (page + 1) * items_per_page
    a = '<div class="admin-popup">'
    a += '<h3>Posts:</h3><a href="/admin/posts/edit"><img class="button" alt="Add a new Post" ' \
         'src="/staticfiles/frontpage/add-post.png"/></a><br />' \
        '<table><tr><th> Post ID </th><th>Post title</th><th> visibility level</th>' \
        '<th> Author </th></tr>'
    objects = Post.objects.filter(pk__range=(start_range, end_range))
    for post in objects:
        a += '<a href="' + generate_edit_link(post) + '"><tr><td>' + str(post.pk) + "</td><td>" + post.title + \
             "</td><td>" + str(post.visibleLevel) + "</td><td>" + str(post.createdByUser.authuser.username) + \
             "</td></tr></a>"
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
