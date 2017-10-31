from django.shortcuts import redirect
from django.http import HttpRequest
from ..models import Article, ArticleMedia, Profile
from .magic import get_current_user, parse_bool
from .magic import compile_markdown
import logging

def action_save_article(request: HttpRequest):
    '''
    This function creates a new or saves an article based on the
    (hopefully) provided POST data elements:
        * price in cents
        * largetext as a markdown text
        * type as a number between 0 and 3 (both inclusive)
        * description a normal text containing the short description
        * visible a bool str if the article should be visible yet
        * quantity the amount of the current aviable pieces
        * size the size of the article (10 char text)
        * [id] the ID of the article to edit (if non is provided
            it will be assumed that it is a new article)
    The user who added the article will be automatically determined.
    The flashImage will be handled by set action_set_image(request)
    If the article to be saved is a newly generated one the function
    will redirect the user to the flash image selection dialog or
    otherwise will redirect the user to the articles page.
    '''
    try:
        price = int(request.GET["price"])
        largetext = request.GET["largetext"]
        article_type = request.GET["type"]
        description = request.GET["description"]
        visible = parse_bool(request.GET["visible"])
        quantity = int(request.GET["quantity"])
        size = request.GET["size"]
        userp: Profile = get_current_user(request)
        aid = -1  # This means that it's a new article
        a: Article = None
        if request.GET.get("id"):
            aid = str("aid")
            a = Article.objects.get(pk=aid)
        else:
            a = Article()
        a.price = price
        a.largeText = largetext
        a.cachedText = compile_markdown(largetext)
        a.type = article_type
        a.description = description
        a.visible = visible
        a.quantity = quantity
        a.size = size
        a.addedByUser = userp
        a.save()
        if aid < 0:
            logging.info("User '" + userp.displayName + "' created a new article (UID: " \
                    + userp.pk + ")")
            return redirect("/admin/media/select")  # TODO fix to correct one
        else:
            logging.info("User '" + userp.displayName + "' modified an article (UID: " \
                    + userp.pk + " AID: " + str(aid) + ")")
            return redirect("/admin/article")
    except Exception as e:
        return redirect('/admin/article/edit?vault=' + str(e))

