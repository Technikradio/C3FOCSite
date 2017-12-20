from django.shortcuts import redirect
from django.http import HttpRequest
from ..models import Article, ArticleMedia, Profile, Media, Settings
from .magic import get_current_user, parse_bool
from .magic import compile_markdown
import logging


def action_save_article(request: HttpRequest):
    """
    This function creates a new or saves an article based on the
    (hopefully) provided POST data elements:
        * price in cents
        * largetext as a markdown text
        * type as a number between 0 and 3 (both inclusive)
        * description a normal text containing the short description
        * visible a bool str if the article should be visible yet
        * quantity the amount of the current aviable pieces
        * size the size of the article (10 char text)
        * [id] (GET) the ID of the article to edit (if non is provided
            it will be assumed that it is a new article)
    The user who added the article will be automatically determined.
    The flashImage will be handled by set action_set_image(request)
    If the article to be saved is a newly generated one the function
    will redirect the user to the flash image selection dialog or
    otherwise will redirect the user to the articles page.
    :param request The current HttpRequest
    :return The crafted response
    """
    try:
        price = request.POST["price"]
        largetext = request.POST["largetext"]
        article_type = request.POST["type"]
        description = request.POST["description"]
        visible = parse_bool(request.POST["visible"])
        quantity = int(request.POST["quantity"])
        size = request.POST["size"]
        userp: Profile = get_current_user(request)
        aid = -1  # This means that it's a new article
        a: Article = None
        if request.GET.get("id"):
            aid = int(request.GET["id"])
            a = Article.objects.get(pk=aid)
        else:
            a = Article()
        a.price = str(price)
        a.largeText = str(largetext)
        a.cachedText = compile_markdown(largetext)
        a.type = int(article_type)
        a.description = str(description)
        a.visible = visible
        a.quantity = int(quantity)
        a.size = str(size)
        a.addedByUser = userp
        a.save()
        if aid < 0:
            logging.info("User '" + userp.displayName + "' created a new article (UID: "
                         + str(userp.pk) + ")")
            return redirect("/admin/media/select")  # TODO fix to correct one (Create handler view in media actions,
            # provide a URL and use it here)
        else:
            logging.info("User '" + userp.displayName + "' modified an article (UID: "
                         + str(userp.pk) + " AID: " + str(aid) + ")")
            return redirect("/admin/articles")
    except Exception as e:
        return redirect('/admin/?error=' + str(e))


def action_change_splash_image(request: HttpRequest):
    try:
        m: Media = Media.objects.get(pk=int(request.GET["media_id"]))
        a: Article = Article.objects.get(pk=int(request.GET["payload"]))
        a.flashImage = m
        a.save()
        return redirect("/admin/articles/edit?id=" + str(a.pk))
        pass
    except Exception as e:
        return redirect("/admin?error=" + str(e))


def action_add_media_to_article(request):
    """
    This action adds the media specified by GET media_id to the article specified by GET payload
    :param request: The HttpRequest
    :return: The crafted response
    """
    try:
        article: Article = Article.objects.get(pk=int(request.GET["payload"]))
        img: Media = Media.objects.get(pk=int(request.GET["media_id"]))
        a: ArticleMedia = ArticleMedia()
        a.MID = img
        a.AID = article
        a.save()
        return redirect("/admin/articles/edit?article_id=" + str(article.pk))
        pass
    except Exception as e:
        return redirect("/admin/?error=" + str(e))


def action_quick_quantity_decrease(request: HttpRequest):
    s: Settings = Settings.objects.get(SName="frontpage.chestsize")
    size: int = int(s.property)
    if not request.GET.get('article_id'):
        return redirect("/admin/?error=BAD_GET_REQUEST")
    try:
        a: Article = Article.objects.get(pk=int(request.GET["article_id"]))
        a.quantity -= size
        a.save()
        return redirect("/admin")
    except Exception as e:
        return redirect("/admin/?error=" + str(e))


