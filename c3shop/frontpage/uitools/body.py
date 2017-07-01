from ..models import Article, Media

DETAILED_PAGE = "/article?id="
NO_MEDIA_IMAGE = "/staticfiles/no-image.png"  # TODO change to static file


def render_article_list():
    #
    # get the first article due to test reasons
    #
    # art = Article.get_next_in_order()
    # return str(art.description)
    a = Article()
    a.description = "Test artikel (generiert)"
    a.type = 0
    a.size = "XXL"
    a.price = "25,00€"
    a.visible = True
    a.quantity = 300
    return render_article_overview(a)


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

