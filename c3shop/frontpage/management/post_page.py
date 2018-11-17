from django.http import HttpRequest
from ..models import Post


def generate_edit_link(p: Post):
    return "/admin/posts/edit?post_id=" + str(p.pk)


def render_post_list(request: HttpRequest):
    # TODO add method to select how many posts to display
    # TODO make layout more fancy
    page = 1
    items_per_page = 50
    if request.GET.get('objects'):
        items_per_page = int(request.GET["objects"])
    total_items = Post.objects.all().count()  # This method isn't totally super dumb since django query sets are lazy.
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
    a = '<div class="admin-popup w3-row w3-padding-64 w3-twothird w3-container">'
    a += '<h3>Posts:</h3>Add Post: <a href="/admin/posts/edit"><img class="button-img" alt="Add a new Post" ' \
         'src="/staticfiles/frontpage/add-post.png"/></a><br />' \
        '<table><tr><th> Edit </th><th> Post ID </th><th>Post title</th><th> visibility level</th>' \
        '<th> Author </th><th> Delete </th></tr>'
    objects = Post.objects.filter(pk__range=(start_range, end_range))
    for post in objects:
        a += '<tr><td><a href="' + generate_edit_link(post) + '"><img src="/staticfiles/frontpage/edit.png" ' \
                    'class="button-img"/></a></td><td>' + str(post.pk) + "</td><td>" + post.title + \
             "</td><td>" + str(post.visibleLevel) + "</td><td>" + str(post.createdByUser.authuser.username) + \
             '</td><td><a href="/admin/confirm?back_url=' + request.path + '&forward_url=/admin/actions/' \
             'delete-post&payload=' + str(post.pk) + '"><img src="/staticfiles/frontpage/delete.png" ' \
                                                     'class="button-img" /></a></td></tr>'
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
