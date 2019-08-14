from django.http import HttpRequest, HttpResponseRedirect
# from django.shortcuts import redirect
from ..models import GroupReservation, ArticleRequested, Article, ArticleGroup
from .magic import get_current_user
import json
import datetime

RESERVATION_CONSTRUCTION_COOKIE_KEY: str = "org.technikradio.c3shop.frontpage" + \
        ".reservation.cookiekey"
EMPTY_COOKY_VALUE: str = '''
{
"notes": "",
"articles": [],
"pickup_date": ""
}
'''


def update_reservation_articles(postdict, rid):
    res: GroupReservation = GroupReservation.objects.get(id=rid)



def add_article_action(request: HttpRequest, default_foreward_url: str):
    forward_url: str = default_foreward_url
    if request.GET.get("redirect"):
        forward_url = request.GET["redirect"]
    else:
        forward_url = "/admin"
    if "rid" not in request.GET:
        return HttpResponseRedirect("/admin?error=Missing%20reservation%20id%20in%20request")
    u: Profile = get_current_user(request)
    current_reservation = GroupReservation.objects.get(id=str(request.GET["rid"]))
    if current_reservation.createdByUser != u and u.rights < 2:
        return HttpResponseRedirect("/admin?error=noyb")
    if current_reservation.submitted == True:
        return HttpResponseRedirect("/admin?error=Already%20submitted")
    # Test for multiple or single article
    if "article_id" in request.POST:
        # Actual adding of article
        aid: int = int(request.GET.get("article_id"))
        quantity: int = int(request.POST["quantity"])
        notes: str = request.POST["notes"]
        ar = ArticleRequested()
        ar.AID = Article.objects.get(id=aid)
        ar.RID = current_reservation
        ar.amount = quantity
        ar.notes = notes
        ar.save()
    # Actual adding of multiple articles
    else:
        if "group_id" not in request.GET:
            return HttpResponseRedirect("/admin?error=missing%20group%20id")
        g: ArticleGroup = ArticleGroup.objects.get(id=int(request.GET["group_id"]))
        for art in Article.objects.all().filter(group=g):
            if str("quantity_" + str(art.id)) not in request.POST or str("notes_" + str(art.id)) not in request.POST:
                return HttpResponseRedirect("/admin?error=Missing%20article%20data%20in%20request")
            amount = int(request.POST["quantity_" + str(art.id)])
            if amount > 0:
                ar = ArticleRequested()
                ar.AID = art
                ar.RID = current_reservation
                ar.amount = amount
                ar.notes = str(request.POST[str("notes_" + str(art.id))])
                ar.save()
    response = HttpResponseRedirect(forward_url + "?rid=" + str(current_reservation.id))
    return response


def write_db_reservation_action(request: HttpRequest):
    """
    This function is used to add a reservation to the database from the
    cookie stored inside the client. This function automatically crafts
    the required HttpResponse.
    """
    u: Profile = get_current_user(request)
    forward_url = "/admin?success"
    if u.rights > 0:
        forward_url = "/admin/reservations"
    if request.GET.get("redirect"):
        forward_url = request.GET["redirect"]
    if "payload" not in request.GET:
        return HttpResponseRedirect("/admin?error=No%20id%20provided")
    current_reservation = GroupReservation.objects.get(id=int(request.GET["payload"]))
    if current_reservation.createdByUser != u and u. rights < 2:
        return HttpResponseRedirect("/admin?error=noyb")
    current_reservation.submitted = True
    current_reservation.save()
    res: HttpResponseRedirect = HttpResponseRedirect(forward_url)
    return res


def manipulate_reservation_action(request: HttpRequest, default_foreward_url: str):
    """
    This function is used to alter the reservation beeing build inside
    a cookie. This function automatically crafts the required response.
    """
    js_string: str = ""
    r: GroupReservation = None
    u: Profile = get_current_user(request)
    if "rid" in request.GET:
        # update reservation
        r = GroupReservation.objects.get(id=int(request.GET["rid"]))
    elif u.number_of_allowed_reservations < GroupReservation.objects.all().filter(createdByUser=u).count():
        r = GroupReservation()
        r.createdByUser = u
        r.ready = False
        r.open = True
        r.pickupDate = datetime.datetime.now()
    else:
        return HttpResponseRedirect("/admin?error=noyb")
    if request.POST.get("notes"):
        r.notes = request.POST["notes"]
    if request.POST.get("contact"):
        r.responsiblePerson = str(request.POST["contact"])
    if (r.createdByUser == u or o.rights > 1) and not r.submitted:
        r.save()
    else:
        return HttpResponseRedirect("/admin?error=noyb")
    forward_url: str = default_foreward_url
    if request.GET.get("redirect"):
        forward_url = request.GET["redirect"]
    response: HttpResponseRedirect = HttpResponseRedirect(forward_url + "?rid=" + str(r.id))
    return response


def action_delete_article(request: HttpRequest):
    """
    This function removes an article from the reservation and returnes
    the required resonse.
    """
    u: Profile = get_current_user(request)
    if "rid" in request.GET:
        response = HttpResponseRedirect("/admin/reservations/edit?rid=" + str(int(request.GET["rid"])))
    else:
        return HttpResponseRedirect("/admin?error=Missing%20reservation%20id%20in%20request")
    if request.GET.get("id"):
        aid: ArticleRequested = ArticleRequested.objects.get(id=int(request.GET["id"]))
        r: GroupReservation = GroupReservation.objects.get(id=int(request.GET["rid"]))
        if (aid.RID.createdByUser == u or u.rights > 1) and aid.RID == r and not r.submitted:
            aid.delete()
        else:
            return HttpResponseRedirect("/admin?error=You're%20not%20allowed%20to%20do%20this")
    return response
