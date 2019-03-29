import traceback

from django.http import HttpRequest
from django.shortcuts import redirect

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


def update_group_metadata(requestdict, grpid: int):
    grp: ArticleGroup = None
    if grpid != -1:
        grp = ArticleGroup.objects.get(id=grpid)
    else:
        grp = ArticleGroup()
    grp.group_name = requestdict["grpname"]
    grp.save()
    articles = Article.objects.all().filter(group=grp)
    defaultprice = requestdict["defaultgrpprice"]
    force = False
    fsvisible = False
    if requestdict.get("forceupdate"):
        force = True
    if requestdict.get("visible"):
        fsvisible = True
    for a in articles:
        mod = False
        if a.price == "0000" or force:
            a.price = defaultprice
            mod = True
        if fsvisible and not a.visible:
            a.visible = True
            mod = True
        if mod:
            a.save()
    return grp.id, defaultprice


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


def release_group(groupid: int):
    grp: ArticleGroup = ArticleGroup.objects.get(id=groupid)
    for a in Article.objects.all().filter(group=grp).filter(underConstruction=True):
        a.underConstruction = False
        a.save()


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


def handle_group_metadata_update(request: HttpRequest):
    groupid: int = -1
    dp = ""
    try:
        groupid = int(request.GET["gid"])
        dp = request.GET["dp"]
    except:
        return redirect("/admin/articles/editgroup?msgid=editgroup.brokenrequest&dp=" + dp)
    try:
        gid, price = update_group_metadata(request.POST.copy(), groupid)
        return redirect("/admin/articles/editgroup?gid=" + str(gid) + "&dp=" + str(price))
    except:
        print("Begin of Trace========================================")
        traceback.print_exc()
        print("END of Trace==========================================")
        return redirect("/admin/articles/editgroup?msgid=editgroup.updatefailed&gid=" + str(groupid) + "&dp=" + dp)


def handle_release_group_request(request: HttpRequest):
    gid: int = -1
    dp = ""
    try:
        gid = int(request.GET["gid"])
        dp = request.GET["dp"]
    except:
        return redirect("/admin/articles/editgroup?msgid=editgroup.brokenrequest&dp=" + dp)
    try:
        release_group(gid)
        return redirect("/admin/articles/editgroup?gid=" + str(gid) + "&dp=" + dp)
    except:
        print("Begin of Trace========================================")
        traceback.print_exc()
        print("END of Trace==========================================")
        return redirect("/admin/articles/editgroup?msgid=editgroup.updatefailed&gid=" + str(gid) + "&dp=" + dp)


