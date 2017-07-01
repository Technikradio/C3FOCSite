from ..models import Article


def render_article_list():
    #
    #get the first article due to test reasons
    #
    art = Article.get_next_in_order()
    return str(art.description)
