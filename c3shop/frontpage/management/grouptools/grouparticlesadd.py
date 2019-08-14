from django.http import HttpRequest
from django.shortcuts import redirect

from frontpage.management.magic import compile_markdown, get_current_user
from frontpage.models import Profile, ArticleGroup, Article


def add_article_to_group(grpid: int, size: str, arttyp: int, user: Profile):
    grp: ArticleGroup = ArticleGroup.objects.get(id=grpid)
    a: Article = Article()
    a.underConstruction = True
    a.group = grp
    a.description = grp.group_name
    a.visible = False
    a.price = "0000"
    a.largeText = "# This group hasn't been updated yet.\nPlease update matrix of group N° " \
            + str(grpid) + "\n<!-- DEFAULT NOIMP TEXT -->"
    a.cachedText = compile_markdown(a.largeText)
    a.type = arttyp
    a.quantity = 0
    a.size = size
    a.addedByUser = user
    a.chestsize = 0
    a.save()


def handle_group_article_add(request: HttpRequest):
    groupid: int = -1
    size = ""
    arttype = 4
    dp = ""
    try:
        groupid = int(request.GET["gid"])
        size = str(request.GET["size"])
        arttype = int(request.GET["type"])
        dp = request.GET["dp"]
    except:
        return redirect("/admin/articles/editgroup?msgid=editgroup.brokenrequest&dp=" + dp)
    add_article_to_group(groupid, size, arttype, get_current_user(request))
    return redirect("/admin/articles/editgroup?gid=" + str(groupid) + "&dp=" + dp)