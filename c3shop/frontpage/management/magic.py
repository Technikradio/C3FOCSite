import markdown
from pyembed.markdown import PyEmbedMarkdown
from django.http import HttpRequest
from ..models import Profile, Article, ArticleRequested


def compile_markdown(markdown_sources: str):
    """
    This function is designed to be a small shortcut for converting md sources to html (required by the caching).
    :param markdown_sources: The markdown source code
    :return: The HTML code
    """
    loaded_extensions = [
        "markdown.extensions.extra",
        "markdown.extensions.admonition",
        "markdown.extensions.toc",
        "markdown.extensions.wikilinks",
        "markdown_checklist.extension",
        "superscript",
        "subscript",
        PyEmbedMarkdown(),
    ]
    return markdown.markdown(markdown_sources, extensions=loaded_extensions)


def get_current_user(request: HttpRequest):
    return Profile.objects.get(authuser=request.user)


def parse_bool(s: str):
    return s in ("yes", "true", "t", "1", "visible")


def get_article_pcs_free(a: Article):
    i: int = a.quantity
    for request in ArticleRequested.objects.all().filter(AID=a):
        # The following isn't ideal du to its heavy db access overhead but I
        # havn't figured something clever out (yet)
        if request.RID.open:
            i -= request.amount
    return i
