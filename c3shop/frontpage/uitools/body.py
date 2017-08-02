from ..models import Article, Media, ArticleMedia, Post, Profile
import logging

SERVER_ROOT = "localhost:8000"
DETAILED_PAGE = SERVER_ROOT + "/article/"  # For example /article/550/
NO_MEDIA_IMAGE = SERVER_ROOT + "/staticfiles/frontpage/no-image.png"  # TODO change to static file


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
        logging.debug("using default image to present article list item")
        pass
    art = '<a href="' + link + '"><article><table><tr><td><img ' \
                               'class="article_list_image" alt="For some weired reason the image is missing" src="'
    art += flash_image_link + '"></td><td>'
    art += '<h3>' + escape_text(target.description) + '</h3><div class="article_list_detail">' + \
           get_type_string(int(target.type)) + " "
    art += escape_text(target.size) + " "
    if target.quantity > 0:
        art += escape_text(target.price) + "<br/>" + str(target.quantity) + " left"
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
        text = "<br/><h2>" + escape_text(art.description) + "</h2><br/>"
        text += render_article_properties_division(art)
        text += render_image(art.flashImage) + "<br />"
        text += '<div class="article_detailed_text_division">' + art.cachedText + "</div><br />"
        logging.debug("Passed introduction list")
        text += render_article_image_list(art)
        logging.debug("Passed image list")
        text += render_user_link(art.addedByUser)
        return text
    except Exception as e:
        return "<br />failed to retrieve article " + str(article_id) + ":<br/>" + str(e)


def render_article_properties_division(art):
    text = '<div class="article_properties_division"><br />Size: '
    text += escape_text(art.size) + "<br />Type: " + get_type_string(int(art.type)) + "<br />Price: " + escape_text(art.price) + "<br />"
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
    text += '<a href="' + SERVER_ROOT + "/user/display/" + str(user.pk) + '">'
    text += render_image(user.avatarMedia, high_res=False)
    text += escape_text(user.displayName)
    text += "</a></div><br/>"
    return text


# TODO implement detailed media view
def render_image(media, width=0, height=0, high_res=True):
    width_str = ""
    height_str = ""
    if width != 0:
        width_str = "width={0}".format(str(width))
        if height != 0:
            height_str = " height={0}".format(str(height))
    elif height != 0:
        height_str = "height={0}".format(str(height))
    if media is None:
        return '<img src="' + NO_MEDIA_IMAGE + '" alt="No suitable image was submitted"/>'
    try:
        if high_res:
            return '<img src="' + media.highResFile + '" alt="This should display an HQ image but' \
                                                      ' something went wrong" ' + width_str + height_str + '/>'
        else:
            return '<img src="' + media.lowResFile + '" alt="This should display an LQ image but' \
                                                     ' something went wrong" ' + width_str + height_str + '/>'
    except Exception as link_exception:
        return '<img src="' + NO_MEDIA_IMAGE + '" alt="No suitable image was located: ' + str(link_exception) + '"/>'


# TODO implement visibility level
def render_post(post_id):
    post = Post.objects.get(pk=post_id)
    time = "No Date available"
    try:
        time = str(post.timestamp)
    except Exception as e:
        logging.debug("While reading the timestamp for the article " + str(post_id) + " an error occurred:")
        logging.debug(str(e))
    text = "<br /><h2>" + escape_text(post.title) + "</h2>"
    text += post.cacheText
    text += "<p>This article was created on " + time + " by:</p>"
    text += render_user_link(post.createdByUser)
    return text


def render_user_detail(user_id):
    user = Profile.objects.get(pk=user_id)
    text = "<h2>" + escape_text(user.displayName) + "</h2>"
    text += render_image(user.avatarMedia)
    text += '<p class="user_meta">Registered since: ' + str(user.creationTimestamp) + "<br />Active: " + \
            str(user.active) + "<br />DECT number: " + str(user.dect) + "</p>"
    text += '<p class="user_notes">' + escape_text(user.notes) + "</p>"
    return text


def escape_text(text):
    """
    This function takes a text and makes it html proof
    :param text: The text to escape
    :return: The escaped text
    """
    return text.replace('<', '&lt;').replace('>', '&gt;')


def require_login(request, min_required_user_rights=0):
    """
    This function makes sure that the current browser is logged in or will otherwise return a redirect response
    :type request: http_request
    :type min_required_user_rights: int
    """
    user_id = request.session["user"]
    if not user_id:
        return True
    user = Profile.objects.get(pk=int(user_id))
    if not user:
        return True
    if user.rights < min_required_user_rights:
        return True
    return False  # makes sure that
