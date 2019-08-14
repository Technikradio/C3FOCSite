import traceback

from django.http import HttpRequest
from django.shortcuts import redirect

from frontpage.models import ArticleGroup, Article


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