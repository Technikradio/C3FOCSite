from ..models import Article, Media, ArticleMedia

DETAILED_PAGE = "/article/"  # For example /article/550/
NO_MEDIA_IMAGE = "/staticfiles/frontpage/no-image.png"  # TODO change to static file


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
        text = "<br/><h2>" + art.description + "</h2><br/>"
        text += render_article_properties_division(art)
        text += render_image(art.flashImage) + "<br />"
        text += '<div class="article_detailed_text_division">' + art.cachedText + "</div><br />"
        print("Passed introduction list")
        text += render_article_image_list(art)
        print("Passed image list")
        text += render_user_link(art.addedByUser)
        return text
    except Exception as e:
        return "<br />failed to retrieve article " + str(article_id) + ":<br/>" + str(e)


def render_article_properties_division(art):
    text = '<div class="article_properties_division"><br />Size: '
    text += art.size + "<br />Type: " + get_type_string(int(art.type)) + "<br />Price: " + art.price + "<br />"
    text += "Pieces left (app.): " + str(art.quantity) + "<br /></div><br />"
    return text


def render_article_image_list(art):
    text = '<div class="article_images_division">'
    article_media = ArticleMedia.objects.filter(AID=art)
    images = []
    for article_image in article_media:
        images.append(article_image.MID)
    for image in images:
        text += render_image(image) + '<br/>'
    text += "</div>"
    return text


def render_user_link(user):
    text = '<div class="user_link_division">'
    text += render_image(user.avatarMedia)
    text += user.displayName
    text += "</div><br/>"
    return text


def render_image(media):
    if media is None:
        return '<img src="' + NO_MEDIA_IMAGE + '" alt="No suitable image was submitted"/>'
    try:
        return '<img src="' + media.highResFile + '" alt="This should display an image but something went wrong"/>'
    except Exception as link_exception:
        return '<img src="' + NO_MEDIA_IMAGE + '" alt="No suitable image was located: ' + str(link_exception) + '"/>'
