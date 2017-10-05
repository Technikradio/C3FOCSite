from django.http import HttpRequest
from ..models import GroupReservation
from ..uitools.body import escape_text


# TODO replace bool str with icon
def render_open_order_table():
    a = '<table class="order_table"><tr><th>Ready</th><th>Pickup date</th><th>Created by User</th></tr>'
    m = GroupReservation.objects.get(open=True).filter(ready=False)
    for o in m:
        a += '<tr><td>' + str(o.ready) + '</td><td>' + str(o.pickupDate) + '</td><td>' + \
             escape_text(o.createdByUser.displayName) + '</td></tr>'
    a += '</table>'
    return a


def generate_edit_link(o: GroupReservation):
    return "/admin/orders/edit?order_id=" + str(o.pk)


def render_order_list(request: HttpRequest):
    # TODO add method to select how many orders to display
    # TODO create icon for adding an order
    # TODO make layout more fancy
    # TODO replace bool str with icon
    page = 1
    items_per_page = 50
    total_items = GroupReservation.objects.all().size()
    max_page = total_items / items_per_page
    if request.GET.get('page'):
        page = int(request.GET["page"])
    if request.GET.get('objects'):
        items_per_page = int(request.GET["objects"])
    if page > max_page:
        page = max_page
    start_range = 1 + page * items_per_page
    end_range = (page + 1) * items_per_page
    a = '<h3>Orders:</h3><a href="/admin/posts/edit">Add a new Order</a>' \
        '<table><tr><th> ID </th><th> Open </th><th> Pickup date </th><th> Issuer </th></tr>'
    objects = GroupReservation.objects.filter(pk__rage=(start_range, end_range))
    for order in objects:
        a += '<a href="' + generate_edit_link(order) + '"><tr><td>' + str(order.pk) + "</td><td> " \
             + str(order.ready) + " </td><td>" + order.pickupDate + "</td><td>" + str(order.createdByUser.displayName) \
             + "</td></tr></a>"
    a += '</table>'
    if page > 1:
        a += '<a href="' + request.path + '?page=' + str(page - 1) + '&objects=' + str(objects) + '" class="button">' \
                                                                                                  'Previous page </a>'
    if page < max_page:
        a += '<a href="' + request.path + '?page=' + str(page + 1) + '&objects=' + str(objects) + '" class="button">' \
                                                                                                  'Next page </a>'
    a += '<center>displaying page ' + str(page) + ' of ' + str(max_page) + ' total pages.</center>'

    return a


def render_order_page(request: HttpRequest):
    a = "<h2>The following orders are still open:</h2>"
    a += render_open_order_table()
    a += "<h2>Below is a list of all orders:"
    a += render_order_list(request)
    return a
