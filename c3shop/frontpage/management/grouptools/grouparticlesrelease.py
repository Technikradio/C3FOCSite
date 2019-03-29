import traceback

from django.http import HttpRequest
from django.shortcuts import redirect

from frontpage.models import ArticleGroup, Article


def release_group(groupid: int):
    grp: ArticleGroup = ArticleGroup.objects.get(id=groupid)
    for a in Article.objects.all().filter(group=grp).filter(underConstruction=True):
        a.underConstruction = False
        a.save()


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