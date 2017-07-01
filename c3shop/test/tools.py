from frontpage.models import Article, User, Media, ArticleMedia, MediaUpload


def make_testing_db():

    m = Media()
    m.headline = "Most ugly image"
    m.lowResFile = "https://example.com/image.jpg"
    m.highResFile = "https://example.com/image.jpg"
    m.save()
    print("media created")

    u = User()
    u.username = "testuser01"
    u.active = True
    u.dect = 5234
    u.displayName = "Test User 01"
    u.rights = 0
    u.save()
    u.avatarMedia = m
    print("User created")

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

