import traceback

from django.http import HttpRequest
from django.shortcuts import redirect

from frontpage.management.grouptools.grouparticlesadd import add_article_to_group
from ..magic import compile_markdown, get_current_user

from frontpage.models import ArticleGroup, Article, Profile

DEFAULT_PRICE_COOKIE_KEY = "net.c3foc.cookies.default_group_price"
DEFAULT_TEXT_COOKIE_KEY = "net.c3foc.cookies.default_group_text"

"""
The default price cookie contains the default price, followed by ':' and the group ID.
This is done in order to make sure that the cookie reflects the current group.
If the edit method detects an invalid ID it will force an update.
The default text cookie gets encoded as follows: <text as UTF8-Base64>:<group ID>
"""


def update_group_article_matrix(requestdict, grpid: int, user: Profile):
    grp: ArticleGroup = ArticleGroup.objects.get(id=grpid)
    arts = Article.objects.all().filter(group=grp)
    totalmod = False
    default_text: str = ""
    default_description: str = ""
    if requestdict.get("defaulttext"):
        default_text = requestdict["defaulttext"]
    if requestdict.get("defaultdescription"):
        default_description = requestdict["defaultdescription"]
    default_cs = int(requestdict["defaultchestsize"])
    if requestdict.get("newsize") and requestdict.get("newtype"):
        ty = int(requestdict["newtype"])
        if ty != -1:
            add_article_to_group(grpid, requestdict["newsize"], ty, user)
    force = False
    if requestdict.get("forceupdate"):
        force = True
    if default_text:
        default_compiled_text = compile_markdown(default_text)
        for a in arts:
            if ("<!-- DEFAULT NOIMP TEXT -->" in a.largeText) or force:
                a.largeText = default_text
                a.cachedText = default_compiled_text
                a.save()
                totalmod = True
    if default_description:
        for a in arts:
            if ((default_description != a.description) and (a.description == grp.group_name)) or force:
                a.description = default_description
                a.save()
                totalmod = True
    for a in arts:
        mod = False
        if a.chestsize == 0 or force:
            a.chestsize = default_cs
            mod = True
        p = requestdict.get("price_" + str(a.size) + "_" + str(a.type))
        q = requestdict.get("quantity_" + str(a.size) + "_" + str(a.type))
        if (p and p != a.price) or (force and (p is not None)):
            a.price = p
            mod = True
        if (q and q != a.quantity) or (force and (q is not None)):
            a.quantity = q
            mod = True
        if mod:
            a.save()
            totalmod = True
    return totalmod


def handle_group_articles_request(request: HttpRequest):
    groupid: int = -1
    msgstr = ""
    dp = ""
    try:
        groupid = int(request.GET["gid"])
        dp = request.GET["dp"]
    except:
        return redirect("/admin/articles/editgroup?msgid=editgroup.brokenrequest&dp=" + dp)
    try:
        if update_group_article_matrix(request.POST.copy(), groupid, get_current_user(request)):
            msgstr = "&success=1&msgid=editgroup.updated"
    except Exception as e:
        # Go back and display an error
        print(e)
        traceback.print_exc()
        return redirect("/admin/articles/editgroup?msgid=editgroup.updatefailed&gid=" + str(groupid) + "&dp=" + dp)
    return redirect("/admin/articles/editgroup?gid=" + str(groupid) + "&dp=" + dp + msgstr)


