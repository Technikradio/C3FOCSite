from django.http import HttpRequest
from ..models import GroupReservation, Profile
from ..uitools.body import escape_text
from .magic import get_current_user
import logging

logger = logging.getLogger(__name__)

def generate_export_link(u: Profile):
    # Check for user rights, collect open reservation id's and generate link
    l = ""
    p = None
    if u.rights > 0:
        p = GroupReservation.objects.filter(open=True).filter(ready=False)
    else:
        return l, p
    m = ""
    for r in p:
        # Iterate through each reservation and add it
        if not m == "":
            m += ','
        m += str(r.id)
    l = '<a href="/admin/export?method=pdf&reservations=' + m + '" class="button">Generate reservations PDF</a><br/><br/><br/>'
    return l, p


def render_open_order_table(u: Profile):
    # We don't have to deal with performance here since it won't get hit that much
    try:
        a, m = generate_export_link(u)
        a += '<table class="order_table"><tr><th>Ready</th><th>Pickup date</th><th>Created by User</th>' \
            '<th>Process</th></tr>'
        p = GroupReservation.objects.all().filter(open=True)
        if u.rights < 1:
            p = p.filter(createdByUser=u)
        if p.count() > 0:
            # m = GroupReservation.objects.filter(open=True).filter(ready=False)
            if u.rights < 1:
                m = m.filter(createdByUser=u)
            for o in m:
                a += '<tr><td>' + generate_order_ready_status_image(o.ready) + '</td><td>' + str(o.pickupDate) + \
                     '</td><td>' + escape_text(o.createdByUser.displayName) + '</td><td><a href="/admin/reservations' \
                     '/process?reservation_id=' + str(o.pk) + '">' \
                     '<img src="/staticfiles/frontpage/process-reservation.png" class="button-img" /></a></td></tr>'
            a += '</table>'
        else:
            a += "</table><h5>You don't have any open reservations at the moment :-)</h5>"
        return a
    except Exception as e:
        logger.exception(e)
        return "Unable to retrieve order data: " + str(e)


def generate_edit_link(o: GroupReservation):
    return "/admin/reservations/edit?id=" + str(o.pk)


def generate_order_ready_status_image(state: bool):
    if state:
        return '<img src="/staticfiles/frontpage/done.png" alt="Ready" class="icon" />'
    else:
        return '<img src="/staticfiles/frontpage/not-done.png" alt="Not yet ready" class="icon" />'


def generate_order_open_status_image(state: bool):
    # TODO find better icons
    if state:
        return '<img src="/staticfiles/frontpage/done.png" alt="Open" class="icon" />'
    else:
        return '<img src="/staticfiles/frontpage/not-done.png" alt="Closed" class="icon" />'


def render_order_list(request: HttpRequest):
    # TODO add method to select how many orders to display
    # TODO create icon for adding an order
    # TODO make layout more fancy
    page = 1
    items_per_page = 50
    total_items = GroupReservation.objects.all().count()
    max_page = total_items / items_per_page
    if max_page < 1:
        max_page = 1
    if request.GET.get('page'):
        page = int(request.GET["page"])
    if request.GET.get('objects'):
        items_per_page = int(request.GET["objects"])
    if page > max_page:
        page = max_page
    start_range = 1 + page * items_per_page
    if start_range > total_items:
        start_range = 0
    end_range = (page + 1) * items_per_page
    a = '<h3>Orders:</h3>' \
        '<table><tr><th> ID </th><th> Open </th><th> Ready </th><th> Pickup date </th><th> Issuer </th>' \
        '<th>Close after pickup</th></tr>'
    objects = GroupReservation.objects.filter(pk__range=(start_range, end_range))
    for order in objects:
        a += '<a href="' + generate_edit_link(order) + '"><tr><td>' + str(order.pk) + "</td><td> " \
             + generate_order_open_status_image(order.open) + " </td><td> " \
             + generate_order_ready_status_image(order.ready) + " </td><td>" + str(order.pickupDate) + "</td><td>" + \
             str(order.createdByUser.displayName) + "</td><td>"
        if order.ready and order.open:
            a += '<a href="/admin/confirm?back_url=' + request.path + '&payload=' + str(order.pk) + \
                 '&forward_url=/admin/actions/close-reservation"><img src="/staticfiles/frontpage/done.png" ' \
                 'class="button-img" /></a>'
        elif not order.ready:
            a += "This reservation isn't ready yet."
        else:
            a += "Already closed."
        a += "</td></tr></a>"
    a += '</table>'
    if page > 1:
        a += '<a href="' + request.path + '?page=' + str(page - 1) + '&objects=' + str(objects) + '" class="button">' \
                                                                                                  'Previous page </a>'
    if page < max_page:
        a += '<a href="' + request.path + '?page=' + str(page + 1) + '&objects=' + str(objects) + '" class="button">' \
                                                                                                  'Next page </a>'
    a += '<center>displaying page ' + str(page) + ' of ' + str(max_page) + ' total pages.</center>'

    return a


def render_personal_req_management(request: HttpRequest):
    a = "<div>"

    a += '<a href="/admin/reservations/edit"><span class="button">Add a new order</span></a>'
    a += "</div>"
    return a


def render_order_page(request: HttpRequest):
    u: Profile = get_current_user(request)
    a = '<div class="w3-row w3-padding-64 w3-twothird w3-container">'
    a += render_personal_req_management(request)
    a += "<h2>The following orders are still open:</h2>"
    a += render_open_order_table(u)
    if u.rights > 0:
        a += "<h2>Below is a list of all orders:</h2>"
        a += render_order_list(request)
    a += "<br /></div><br />"
    return a
