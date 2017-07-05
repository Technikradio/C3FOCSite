from ..models import Article, Media

DETAILED_PAGE = "/article/"  # For example /article/550/
NO_MEDIA_IMAGE = "/staticfiles/no-image.png"  # TODO change to static file


def render_article_list():
    a = ""
    for art in Article.objects.all():
        if art.visible:
            a += render_article_overview(art)
    return a


def render_article_overview(target):
    simage = target.flashImage
    link = DETAILED_PAGE + str(target.id)
    flash_image_link = NO_MEDIA_IMAGE
    try:
        flash_image_link = str(simage.highResFile)
    except:
        print("using default image to present article list item")
        pass
    art = '<a href="' + link + '"><article><table><tr><td><img ' \
                               'class="article_list_image" alt="For some weired reason the image is missing" src="'
    art += flash_image_link + '"></td><td>'
    art += '<h3>' + target.description + '</h3><div class="article_list_detail">' + \
           get_type_string(int(target.type)) + " "
    art += target.size + " "
    if target.quantity > 0:
        art += target.price + "<br/>" + str(target.quantity) + " left"
    else:
        art += "<br/>sold out"
    art += "</div></td></tr></table></article></a>"
    return art


def get_type_string(type_sym):
    if type_sym == 0:
        return "Unisex"
    if type_sym == 1:
        return "Female"
    if type_sym == 2:
        return "Male"
    if type_sym == 3:
        return "Kids"


def render_article_detail(article_id):
    try:
        art = Article.objects.get(pk=article_id)
        return "showing article '" + art.description + ".<br/>"
    except Exception as e:
        return "failed to retrieve article " + str(article_id) + ":<br/>" + str(e)

