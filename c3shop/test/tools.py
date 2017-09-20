from frontpage.models import Article, Profile, Media, ArticleMedia, MediaUpload, Post, Settings
from django.contrib.auth.models import User


# This function assumes that the create superuser command has already been run.
def make_testing_db():

    m = Media()
    m.headline = "Most ugly image"
    m.lowResFile = "https://example.com/image.jpg"
    m.highResFile = "https://example.com/image.jpg"
    m.save()
    print("media created")

    u = Profile()
    u.authuser = User.objects.all()[0]
    u.active = True
    u.dect = 5234
    u.displayName = "Test Profile 01"
    u.rights = 0
    u.avatarMedia = m
    u.notes = "<center>This is to test html insertion</center>"
    u.save()
    print("Profile created")

    a = Article()
    a.cachedText = "<h2>This is a dummy article due to testing purposes</h2>"
    a.description = "Test article"
    a.price = "$15.00"
    a.quantity = 1000
    a.size = "XXL"
    a.type = 1
    a.visible = True
    a.addedByUser = u
    a.save()
    print("Article created")

    am = ArticleMedia()
    am.AID = a
    am.MID = m
    am.save()
    print("Article media link created")

    mu = MediaUpload()
    mu.MID = m
    mu.UID = u
    mu.save()
    print("Media user link created")

    p = Post()
    p.title = "Test post 01"
    p.cacheText = "<p>this is a test post<br/>generated by tools.make_testing_db()</p>"
    p.createdByUser = u
    p.visibleLevel = 0

    s = Settings()
    s.changedByUser = u
    s.property = '''[{
            "type":"link",
            "href":"example.com","text":"Visit example.com"
        },{"type":"link","text":"Visit the top level website",
        "href":".."}]'''
    s.SName = 'frontpage.ui.navbar.content'
    s.requiredLevel = 0
    s.save()
    print("NavBar setting created")
