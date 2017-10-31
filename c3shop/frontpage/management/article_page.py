from ..models import Article, Profile
from django.http import HttpRequest
from .magic import get_current_user


def render_article_page(request: HttpRequest):
    u: Profile = get_current_user(request)
    a = '<h3>Articles</h3><br/><a href="" class="button">Add a new Article</a><br/>'
    return a

