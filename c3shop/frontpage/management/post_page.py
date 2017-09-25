from django.http import HttpRequest
from ..models import Post


def generate_edit_link(p: Post):
    return "/admin/posts/edit?post_id=" + str(p.pk)


def render_post_list(request: HttpRequest):
    # TODO add method to select how many posts to display
    # TODO create icon for post writing
    # TODO add way to determine maximum page
    # TODO make layout more fancy
    page = 1
    items_per_page = 50
    if request.GET.get('page'):
        page = int(request.GET["page"])
    if request.GET.get('objects'):
        items_per_page = int(request.GET["objects"])
    start_range = 1 + page * items_per_page
    end_range = (page + 1) * items_per_page
    a = '<h3>Posts:</h3><a href="/admin/posts/edit">Add a new Post</a>' \
        '<table><tr><th> Post ID </th><th>Post title</th><th> visibility level</th>' \
        '<th> Author </th></tr>'
    objects = Post.objects.filter(pk__rage=(start_range, end_range))
    for post in objects:
        a += '<a href="' + generate_edit_link(post) + '"><tr><td>' + str(post.pk) + "</td><td>" + post.title + \
             "</td><td>" + str(post.visibleLevel) + "</td><td>" + str(post.createdByUser.authuser.username) + \
             "</td></tr></a>"
    a += '</table>'
    if page > 1:
        a += '<a href="' + request.path + '?page=' + str(page - 1) + '&objects=' + str(objects) + '">Previous page </a>'
    a += '<a href="' + request.path + '?page=' + str(page + 1) + '&objects=' + str(objects) + '">Next page </a>'
    a += '<center>displaying page ' + str(page) + '.</center>'

    return a
