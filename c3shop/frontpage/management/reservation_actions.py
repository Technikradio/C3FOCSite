from django.http import HttpRequest, HttpResponseRedirect
# from django.shortcuts import redirect
from ..models import GroupReservation, ArticleRequested, Article
from .magic import get_current_user
import json

RESERVATION_CONSTRUCTION_COOKIE_KEY: str = "org.technikradio.c3shop.frontpage" + \
        ".reservation.cookiekey"
EMPTY_COOKY_VALUE: str = '''
{
"notes": "",
"articles": [],
"pickup_date": "",
}
'''


def add_article_action(request: HttpRequest, default_foreward_url: str):
    forward_url: str = default_foreward_url
    if request.GET.get("redirect"):
        forward_url = request.GET["redirect"]
    current_reservation = json.loads(request.COOKIES.get(RESERVATION_CONSTRUCTION_COOKIE_KEY))
    aid: int = int(request.POST.get("article_id"))
    quantity : int = int(request.POST["quantity"])
    notes: str = request.POST["notes"]
    current_reservation.get("articles").append({"id": aid, "quantity": quantity, "notes": notes})
    response = HttpResponseRedirect(forward_url)
    response.set_cookie(RESERVATION_CONSTRUCTION_COOKIE_KEY, json.dumps(current_reservation, indent=4))
    return response


def write_db_reservation_action(request: HttpRequest):
    """
    This function is used to add a reservation to the database from the
    cookie stored inside the client. This function automatically crafts
    the required HttpResponse.
    """
    forward_url = "/admin/reservations"
    if request.GET.get("redirect"):
        forward_url = request.GET["redirect"]
    current_reservation = json.loads(request.COOKIES.get(RESERVATION_CONSTRUCTION_COOKIE_KEY))
    r: GroupReservation = None
    fresh: bool = False
    if not request.GET.get("id"):
        r = GroupReservation()
        fresh = True
    else:
        r = GroupReservation.objects.get(pk=int(request.GET["id"]))
    r.createdByUser = get_current_user()
    r.open = True
    r.notes = current_reservation.get("notes")
    r.pickupDate = current_reservation.get("pickup_date")  # TODO parse to date
    r.ready = False
    r.save()
    for arts in current_reservation.get("articles"):
        aid = int(arts.get("id"))
        q = int(arts.get("quantity"))
        notes = arts.get("notes")
        a: Article = Article.objects.get(pk=aid)
        req: ArticleRequested = None
        if fresh:
            req = ArticleRequested()
        else:
            if ArticleRequested.objects.all().filter(AID=a).filter(RID=r).count() > 0:
                req = ArticleRequested.objects.all().filter(AID=a).filter(RID=r)[0]
            else:
                req = ArticleRequested()
        req.RID = r
        req.AID = a
        req.amount = q
        req.notes = notes
        req.save()
    # Do not simply redirect but also delete the construction cookie
    res: HttpResponseRedirect = HttpResponseRedirect(forward_url)
    res.delete_cookie(RESERVATION_CONSTRUCTION_COOKIE_KEY)
    return res


def manipulate_reservation_action(request: HttpRequest, default_foreward_url: str):
    """
    This function is used to alter the reservation beeing build inside
    a cookie. This function automatically crafts the required response.
    """
    js_string: str = ""
    if request.COOKIES.get(RESERVATION_CONSTRUCTION_COOKIE_KEY):
        js_string = request.COOKIES.get(RESERVATION_CONSTRUCTION_COOKIE_KEY)
    else:
        js_string = EMPTY_COOKY_VALUE
    current_reservation = json.loads(js_string)
    if request.POST.get("notes"):
        current_reservation["notes"] = request.POST["notes"]
    if request.POST.get("pickup_date"):
        current_reservation["pickup_date"] = request.POST["pickup_date"]
    forward_url: str = default_foreward_url
    if request.GET.get("redirect"):
        forward_url = request.GET["redirect"]
    response: HttpResponseRedirect = HttpResponseRedirect(forward_url)
    response.set_cookie(RESERVATION_CONSTRUCTION_COOKIE_KEY, json.dumps(current_reservation, indent=4))
    return response

