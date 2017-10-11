from django.http import HttpRequest
from django.http import HttpResponseNotAllowed
from django.http import HttpResponse
from ..models import Media
from .page_skeleton import render_headbar, render_footer


def render_media_selection_page(request: HttpRequest):
    # TODO add 'add_media' button
    if not request.GET.get('action_url'):
        return HttpResponseNotAllowed("You must specify a action url")
    payload = request.GET.get("payload")
    action_url = request.GET["action_url"]
    action = action_url + "?payload=" + str(payload) + "&media_id="
    page = 1
    if request.GET.get('page'):
        page = int(request.GET['page'])
    items_per_page = 50
    if request.GET.get('objects'):
        items_per_page = int(request.GET["objects"])
    total_items = Media.objects.all().count()
    max_page = total_items / items_per_page
    if page > max_page:
        page = max_page
    start_range = 1 + page * items_per_page
    end_range = (page + 1) * items_per_page
    a = render_headbar(request, title="Select media")
    a += '<div class="admin-popup">'
    a += '<h3>Please select your desired image</h3><table><tr><th>Select</th><th>Preview</th><th>Title</th></tr>'
    objects = Media.objects.filter(pk__range=(start_range, end_range))
    for img in objects:
        a += '<tr><td><a href="' + action + str(img.pk)
        a += '"><img src="/staticfiles/frontpage/add-image.png" class="button"/></a></td><td><img src="'
        a += img.lowResFile + '" /></td><td>' + img.headline + '</td></tr>'
    a += '</table>'
    if page > 1:
        a += '<a href="' + request.path + '?page=' + str(page - 1) + '&objects=' + str(objects) + '&payload=' + \
             str(payload) + '&action_url=' + str(action_url) + '" class="button">Previous page </a>'
    if page < max_page:
        a += '<a href="' + request.path + '?page=' + str(page + 1) + '&objects=' + str(objects) + '&payload=' + \
             str(payload) + '&action_url=' + str(action_url) + '" class="button">Next page </a>'
    a += '</div>' + render_footer(request)
    return HttpResponse(a)
