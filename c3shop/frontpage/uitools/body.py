from django.core.exceptions import ObjectDoesNotExist

from ..models import Article, Media, ArticleMedia, Post, Profile, Settings
from ..management.magic import get_current_user
from django.conf import settings
from django.shortcuts import redirect
from django.http.response import Http404
from django.http import HttpRequest
import logging

SERVER_ROOT = "localhost:8000"
DETAILED_PAGE = SERVER_ROOT + "/article/"  # For example /article/550/
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
        logging.debug("using default image to present article list item")
        pass
    art = '<a href="' + link + '"><article><table><tr><td><img ' \
                               'class="article_list_image" alt="For some weired reason the image is missing" src="'
    art += flash_image_link + '"></td><td>'
    art += '<h3 class="w3-text-teal">' + escape_text(target.description) 
    art += '</h3><div class="article_list_detail">' + get_type_string(int(target.type)) + " "
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


def get_right_string(rights):
    if rights == 0:
        return "unprivileged"  # He isn't allowed to do anything
    if rights == 1:
        return "normal user"  # He is allowed to make team orders
    if rights == 2:
        return "shop manager"  # He is also allowed to manage the article db
    if rights == 3:
        return "author"  # He is allowed to manage articles
    if rights == 4:
        return "admin"  # He is allowed to do anything


def render_article_detail(article_id):
    try:
        art = Article.objects.get(pk=int(article_id))
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


def render_image(media, width=0, height=0, high_res=True, include_link=True, replace: str = ""):
    width_str = ""
    height_str = ""
    if width != 0:
        width_str = "width={0}".format(str(width))
        if height != 0:
            height_str = " height={0}".format(str(height))
    elif height != 0:
        height_str = "height={0}".format(str(height))
    alt_img = NO_MEDIA_IMAGE
    if not replace == "":
        alt_img = replace
    if media is None:
        return '<img src="' + alt_img + '" alt="No suitable image was submitted"/>'
    lb = ""
    a = ""
    if include_link:
        lb = '<a href="/media/' + str(media.pk) + '">'
        a = "</a>"
    try:
        if high_res:
            return lb + '<img src="' + media.highResFile + '" alt="This should display an HQ image but' \
                                                      ' something went wrong" ' + width_str + height_str + '/>' + a
        else:
            return lb + '<img src="' + media.lowResFile + '" alt="This should display an LQ image but' \
                                                     ' something went wrong" ' + width_str + height_str + '/>' + a
    except Exception as link_exception:
        return '<img src="' + NO_MEDIA_IMAGE + '" alt="No suitable image was located: ' + str(link_exception) + '"/>'


# TODO implement visibility level
def render_post(post_id, request: HttpRequest):
    # post: Post = None
    try:
        post = Post.objects.get(pk=int(post_id))
    except ObjectDoesNotExist as e:
        # TODO think about something better when the required post was deleted
        return '<div class="error-panel">The object you\'re looking for seams to be banished in the ether.:<br/>'\
               + str(post_id) + ": " + str(e) + "</div>"
    if post.visibleLevel > 0:
        # Check if user is allowed to see this post
        if not request.user.is_authenticated():
            return ""
        else:
            if get_current_user(request).rights < post.visibleLevel:
                return "You don't have the required permission in order to review this item."
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
    user = Profile.objects.get(pk=int(user_id))
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
    return str(text.replace('<', '&lt;').replace('>', '&gt;'))


def require_login(request, min_required_user_rights=0):
    """
    This function makes sure that the current browser is logged in or will otherwise return a redirect response
    :type request: http_request
    :type min_required_user_rights: int
    """
    if not request.user.is_authenticated():
        return redirect('%s?next="%s"' % (settings.LOGIN_URL, request.path))

    profile = Profile.objects.get(authuser=request.user)
    if not profile:
        return redirect('%s?next="%s"' % (settings.LOGIN_URL, request.path))
    if profile.rights < min_required_user_rights:
        return redirect('%s?next="%s"' % (settings.LOGIN_URL, request.path))
    return False  # makes sure that


def render_user_list(request, objects_per_site=50):
    page = 0
    if request.GET.get('page'):
        page = int(request.GET['page'])
        logging.debug("Displaying page " + str(page))
    # calculating the users to display on the requested page
    start = page * objects_per_site
    end = ((page + 1) * objects_per_site) - 1
    a = '<div class="user_list">'
    a += '<a href="/admin/users/edit"><img class="button" src= "/staticfiles/frontpage/add-user.png" alt="Add user" />'\
         '</a><br />Displaying page ' + str(page) + ' with ' + str(objects_per_site) + ' entries per each.' \
         '<br /><table><tr><th>Edit</th><th>Avatar</th><th>Username</th><th>Display name</th>' \
         '<th>Rights</th></tr>'
    for p in Profile.objects.filter(pk__range=(start, end)):
        # TODO generate link to detailed user view
        a += '<tr><td><a href="/admin/users/edit?user_id=' + str(p.pk) + \
             '"><img class="button" src="/staticfiles/frontpage/edit.png" />' \
            '</a></td><td>' + render_image(p.avatarMedia, width=24, height=24,
                                           replace="/staticfiles/frontpage/no-avatar.png") + '</td><td>' + \
             escape_text(p.authuser.username) + '</td><td>' + escape_text(p.displayName) + '</td><td>' + \
             str(get_right_string(p.rights)) + '</td></tr>'
    a += '</table></div>'
    return a


def render_image_detail(request, medium_id):
    image = Media.objects.get(pk=int(medium_id))
    if image is None:
        raise Http404("No media found")
    a = "<h2>" + image.headline + "</h2><center>"
    a += render_image(image)
    a += "</center><article>" + image.cachedText + "</article>"
    return a


def render_404_page(request):
    return '<h2>This is not the site you\'re looking for</h2><br>You tried to open the following path:<br/><br/>"' + \
           request.path + '"<br/><br />...but it doesn\'t seam to exist.'


def render_index_page(request):
    a = ""
    if Settings.objects.get(SName="frontpage.store.open").property.lower() in ("yes", "true", "t", "1"):
        a += '<div><img src="/staticfiles/frontpage/store-open.png"/>The store is currently open</div>'
    else:
        a += '<div><img src="/staticfiles/frontpage/store-closed.png"/>The store is currently closed.</div>'
    a += render_article_list()
    # Render last 5 posts
    post_ids = []
    size = Post.objects.all().count()
    post_count = 5
    if post_count > size:
        post_count = size
    for i in range(0, post_count):
        post_ids.append(size - i)
    for pid in post_ids:
        a += render_post(pid, request)
    return a
