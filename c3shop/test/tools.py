from frontpage.models import Article, User, Media, ArticleMedia, MediaUpload


def make_testing_db():

    u = User()
    u.username = "testuser01"
    u.active = True
    u.dect = 5234
    u.displayName = "Test User 01"
    u.rights = 0
    u.save()

    m = Media()
    m.headline = "Most ugly image"
    m.lowResFile = "https://example.com/image.jpg"
    m.highResFile = "https://example.com/image.jpg"
    m.save()

    a = Article()
    a.cachedText = "<h2>This is a dummy article due to testing purposes</h2>"
    a.description = "Test article"
    a.price = "$15.00"
    a.quantity = 1000
    a.size = "XXL"
    a.type = "Male"
    a.visible = True
    a.addedByUser = u
    a.save()

    am = ArticleMedia()
    am.AID = a
    am.MID = m
    am.save()

    mu = MediaUpload()
    mu.MID = m
    mu.UID = u
    mu.save()

