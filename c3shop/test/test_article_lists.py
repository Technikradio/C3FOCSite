from django.test import TestCase

from frontpage.uitools.body import render_price, get_type_string, get_right_string
from frontpage.uitools.body import render_article_properties_division
from frontpage.models import Article


class TestManagementGenericFunctions(TestCase):
    def setUp(self):
        # Setup test articles

        pass


    def test_price_rendering(self):
        self.assertEquals(render_price('00'), '0.00 €')
        self.assertEquals(render_price('3005'), '30.05 €')
        self.assertEquals(render_price('-15'), '-0.15 €')
        self.assertEquals(render_price('2300', currency="$"), '23.00 $')


    def test_cloth_type_generation(self):
        self.assertEquals(get_type_string(0), "Unisex")
        self.assertEquals(get_type_string(1), "Female")
        self.assertEquals(get_type_string(2), "Male")
        self.assertEquals(get_type_string(3), "Kids")
        self.assertEquals(get_type_string(4), "Aliens")


    def test_user_priv_string_generation(self):
        self.assertEquals(get_right_string(0), "normal user")
        self.assertEquals(get_right_string(1), "FOC Angel")
        self.assertEquals(get_right_string(2), "shop manager")
        self.assertEquals(get_right_string(3), "author")
        self.assertEquals(get_right_string(4), "admin")


    def test_article_detail_rendering(self):
        a: Article = Article()
        a.size = ">XXL"
        a.type = 3
        a.price = "1337"
        a.quantity = "250"
        self.assertEquals(render_article_properties_division(a),
                '<div class="article_properties_division"><br />Size: &gt;XXL<br />Type: ' + 
                'Kids<br />Price: 13.37 €<br />Pieces left (app.): 250<br /></div><br />')

