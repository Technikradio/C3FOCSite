from django.test import TestCase

from frontpage.models import Article, ArticleGroup
from frontpage.management.grouptools.edit_group import get_article_dict, get_default_description


class TestGroupMatrix(TestCase):
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
        a.visible = True
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
        a.visible = True
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
        a.visible = True
        a.cachedText = "A long text"
        a.chestsize = 100
        a.underConstruction = True
        a.save()
        pass


    def test_article_group_dictionary(self):
        sizes, types, dictionary = get_article_dict(ArticleGroup.objects.all()[0])
        # Due to django clean up there shouldn't be any further groups
        self.assertEquals(sizes, ["S", "XXL"])
        self.assertEquals(types, [2, 3])
        self.assertEquals(dictionary, {
            "S": {2: (169, "1111", 4, "A description", True),
                3: (250, "2500", 2, "A description", True)},
            "XXL": {2: (1313, "1337", 3, "A description", True),
                3: (100, "3000", 1, "A different description", False)}})

    def test_default_description(self):
        self.assertEquals(get_default_description(ArticleGroup.objects.all()[0]),
                          ("A description", 100, "A long text"))
