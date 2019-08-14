from django.test import TestCase

from frontpage.models import Article, ArticleGroup, GroupReservation, ArticleRequested
from frontpage.management.articletools.article_select import get_group_variations
from frontpage.management.magic import get_article_pcs_free
from frontpage.uitools.body import get_type_string

#from .tools import make_testing_db
#from .init_database import init_db

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
        #init_db()
        #make_testing_db()
        pass


    def test_group_vars_generation(self):
        sizes, types = get_group_variations(ArticleGroup.objects.all()[0])
        self.assertTrue(" S XXL " == sizes)
        self.assertTrue(" " + get_type_string(2) + " " + get_type_string(3) + " " == types)

    def test_reservation_group_append(self):
        pass

    def test_reservation_single_append(self):
        pass

    def test_reservation_article_decrease(self):
        a: Article = Article.objects.get(pk=1)
        self.assertEqual(get_article_pcs_free(a), 100)
        res: GroupReservation = GroupReservation()
        res.ready = False
        res.open = True
        res.notes = ""
        res.submitted = True
        import datetime
        res.pickupDate = datetime.datetime.now()
        res.save()
        req: ArticleRequested = ArticleRequested()
        req.RID = res
        req.AID = a
        req.amount = 15
        req.notes = ""
        req.save()
        self.assertEqual(get_article_pcs_free(a), 85)


