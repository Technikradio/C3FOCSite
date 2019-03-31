from django.test import TestCase

from frontpage.models import Article, ArticleGroup
from frontpage.management.articletools.article_select import get_group_variations
from frontpage.uitools.body import get_type_string

class TestReservationEditing(TestCase):
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


    def test_group_vars_generation(self):
        sizes, types = get_group_variations(ArticleGroup.objects.all()[0])
        self.assertTrue(" S XXL " == sizes)
        self.assertTrue(" " + get_type_string(2) + " " + get_type_string(3) + " " == types)

