from django.test import TestCase

from frontpage.models import Article, ArticleGroup, Profile
from frontpage.management.grouptools.grouparticlesupdate import add_article_to_group, release_group, update_group_metadata
from frontpage.management.grouptools.grouparticlesupdate import update_group_article_matrix


class TestArticleGroupManagement(TestCase):
    def setUp(self):
        # Setup test articles
        g: ArticleGroup = ArticleGroup()
        g.group_name = "Test Group"
        g.save()
        a: Article = Article()
        a.size = "XXL"
        a.type = 3
        a.price = "3000"
        a.quantity = 100
        a.group = g
        a.largeText = "A long text"
        a.description = "A different description"
        a.visible = False
        a.cachedText = "A long text"
        a.chestsize = 100
        a.underConstruction = True
        a.save()
        a = Article()
        a.size = "S"
        a.type = 3
        a.price = "2500"
        a.quantity = 250
        a.group = g
        a.largeText = "A long text"
        a.description = "A description"
        a.visible = False
        a.cachedText = "A long text"
        a.chestsize = 102
        a.underConstruction = True
        a.save()
        a = Article()
        a.size = "XXL"
        a.type = 2
        a.quantity = 1313
        a.price = "1337"
        a.group = g
        a.largeText = "A long text"
        a.description = "A description"
        a.visible = False
        a.cachedText = "A long text"
        a.chestsize = 100
        a.underConstruction = True
        a.save()
        a = Article()
        a.size = "S"
        a.type = 2
        a.quantity = 169
        a.price = "1111"
        a.group = g
        a.largeText = "A long text"
        a.description = "A description"
        a.visible = False
        a.cachedText = "A long text"
        a.chestsize = 100
        a.underConstruction = True
        a.save()
        pass


    def test_article_add(self):
        grp: ArticleGroup = ArticleGroup.objects.all()[0]
        add_article_to_group(grp.id, "XL", 2, None)
        a: Article = Article.objects.all().filter(group=grp).filter(size="XL")[0]
        self.assertTrue(a.underConstruction)
        self.assertTrue(str(grp.id) in a.cachedText)
        self.assertTrue("<!-- DEFAULT NOIMP TEXT -->" in a.largeText)
        self.assertFalse(a.visible)
        self.assertEquals(a.price, "0000")
        self.assertEquals(a.type, 2)
        self.assertEquals(a.size, "XL")

    def test_article_release(self):
        grp: ArticleGroup = ArticleGroup.objects.all()[0]
        arts = Article.objects.all().filter(group=grp)
        for a in arts:
            self.assertTrue(a.underConstruction)
        release_group(grp.id)
        arts = Article.objects.all().filter(group=grp)
        for a in arts:
            self.assertFalse(a.underConstruction)

    def test_update_group_metadata(self):
        grp: ArticleGroup = ArticleGroup.objects.all()[0]
        priorCount: int = ArticleGroup.objects.all().count()
        rdict = {"grpname": "A group to add",
                "defaultgrpprice": "666"}
        self.assertEquals(ArticleGroup.objects.all()[ArticleGroup.objects.all().count() - 1].group_name, "Test Group")
        update_group_metadata(rdict, -1)
        self.assertEquals(ArticleGroup.objects.all()[ArticleGroup.objects.all().count() - 1].group_name, "A group to add")
        self.assertEquals(priorCount + 1, ArticleGroup.objects.all().count())
        for a in Article.objects.all().filter(group=grp):
            self.assertFalse(a.visible)
            self.assertNotEquals(a.price, "666")
        update_group_metadata(rdict, grp.id)
        for a in Article.objects.all().filter(group=grp):
            self.assertFalse(a.visible)
            self.assertNotEquals(a.price, "666")
        rdict["visible"] = True
        update_group_metadata(rdict, grp.id)
        for a in Article.objects.all().filter(group=grp):
            self.assertTrue(a.visible)
            self.assertNotEquals(a.price, "666")
        rdict["forceupdate"] = True
        update_group_metadata(rdict, grp.id)
        for a in Article.objects.all().filter(group=grp):
            self.assertTrue(a.visible)
            self.assertEquals(a.price, "666")
        rdict["forceupdate"] = False
        self.assertEquals(grp.group_name, "Test Group")
        rdict["grpname"] = "Another group name"
        update_group_metadata(rdict, grp.id)
        grp: ArticleGroup = ArticleGroup.objects.get(id=grp.id)
        self.assertEquals(grp.group_name, "Another group name")
        rdict["defaultgrpprice"] = "8888"
        update_group_metadata(rdict, grp.id)
        for a in Article.objects.all().filter(group=grp):
            self.assertTrue(a.visible)
            self.assertEquals(a.price, "666")
        add_article_to_group(grp.id, "XL", 2, None)
        self.assertEquals(Article.objects.all().filter(group=grp)[
            Article.objects.all().filter(group=grp).count() -1].price, "0000")
        update_group_metadata(rdict, grp.id)
        self.assertEquals(Article.objects.all().filter(group=grp)[
            Article.objects.all().filter(group=grp).count() -1].price, "8888")


    def test_matrix_update(self):
        grp: ArticleGroup = ArticleGroup.objects.get(id=1)
        rdict = {"defaulttext": "A default updated text",
                "defaultchestsize": "13"}
        for a in Article.objects.all().filter(group=grp):
            self.assertNotEquals(a.largeText, "A default updated text")
        update_group_article_matrix(rdict, grp.id, None)
        for a in Article.objects.all().filter(group=grp):
            self.assertNotEquals(a.largeText, "A default updated text")
        rdict["forceupdate"] = True
        update_group_article_matrix(rdict, grp.id, None)
        for a in Article.objects.all().filter(group=grp):
            self.assertEquals(a.largeText, "A default updated text")
        rdict["forceupdate"] = False
        rdict["defaultdescription"] = "A total silly description"
        for a in Article.objects.all().filter(group=grp):
            self.assertNotEquals(a.description, "A total silly description")
        update_group_article_matrix(rdict, grp.id, None)
        for a in Article.objects.all().filter(group=grp):
            self.assertNotEquals(a.description, "A total silly description")
        rdict["forceupdate"] = True
        update_group_article_matrix(rdict, grp.id, None)
        for a in Article.objects.all().filter(group=grp):
            self.assertEquals(a.description, "A total silly description")
        self.assertEquals(Article.objects.all().filter(group=grp).filter(size="Your size").filter(type=3).count(), 0)
        rdict["newsize"] = "Your size"
        rdict["newtype"] = 3
        rdict["forceupdate"] = False
        update_group_article_matrix(rdict, grp.id, None)
        self.assertEquals(Article.objects.all().filter(group=grp).filter(size="Your size").filter(type=3).count(), 1)
        rdict["newsize"] = None
        rdict["newtype"] = None
        self.assertFalse("<!-- DEFAULT NOIMP TEXT -->" in
                Article.objects.all().filter(group=grp).filter(size="Your size").filter(type=3)[0].largeText,
                "This should automatically resolve the text")
        add_article_to_group(grp.id, "Your size", 2, None)
        self.assertTrue("<!-- DEFAULT NOIMP TEXT -->" in
                Article.objects.all().filter(group=grp).filter(size="Your size").filter(type=2)[0].largeText)
        self.assertEquals(Article.objects.all().filter(group=grp).filter(size="Your size").filter(type=2)[0].chestsize, 0)
        update_group_article_matrix(rdict, grp.id, None)
        self.assertFalse("<!-- DEFAULT NOIMP TEXT -->" in
                Article.objects.all().filter(group=grp).filter(size="Your size").filter(type=2)[0].largeText,
                "This should have been updated yet.")
        self.assertEquals(Article.objects.all().filter(group=grp).filter(size="Your size").filter(type=2)[0].chestsize, 13)
        self.assertTrue(Article.objects.all().filter(group=grp).filter(size="XXL").filter(type=3)[0].price == "3000")
        self.assertTrue(Article.objects.all().filter(group=grp).filter(size="XXL").filter(type=3)[0].quantity == 100)
        rdict["price_XXL_3"] = "2999"
        rdict["quantity_XXL_3"] = "144"
        update_group_article_matrix(rdict, grp.id, None)
        self.assertTrue(Article.objects.all().filter(group=grp).filter(size="XXL").filter(type=3)[0].price == "2999")
        self.assertTrue(Article.objects.all().filter(group=grp).filter(size="XXL").filter(type=3)[0].quantity == 144)
        rdict["price_XXL_3"] = "3000"
        rdict["quantity_XXL_3"] = "100"
        update_group_article_matrix(rdict, grp.id, None)
        self.assertTrue(Article.objects.all().filter(group=grp).filter(size="XXL").filter(type=3)[0].price == "3000")
        self.assertTrue(Article.objects.all().filter(group=grp).filter(size="XXL").filter(type=3)[0].quantity == 100)

