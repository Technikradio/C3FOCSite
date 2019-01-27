from django.test import TestCase  # , Client
from frontpage.models import Article, Post, Media
from frontpage.uitools.searching import perform_query_helper

class SearchArticleTestCase(TestCase):
    def setUp(self):
        Article.objects.create(
                largeText="Test Case Article 1",
                type=1,
                price="2000",
                description="Testshirt 1",
                visible=True,
                quantity=1500,
                size="2XL",
                cachedText="Test Case Article 1",
                chestsize=50
            )
        Article.objects.create(
                description="Test Case Article 2",
                type=1,
                price="4500",
                largeText="A random test Zipper",
                visible=False,
                quantity=350,
                size="M",
                cachedText="A random test Zipper",
                chestsize=35
            )
        Article.objects.create(
                description="Test Case Article 3",
                type=1,
                price="3500",
                largeText="A test case hoody",
                visible=True,
                quantity=0,
                size="L",
                cachedText="A test case hoody",
                chestsize=15
            )
        Post.objects.create(
                title="Test case post 1",
                cacheText="A random test case post",
                text="A random test case post",
                visibleLevel=0,
            )
        Post.objects.create(
                cacheText="Test case post 2",
                title="Test post N° 2",
                text="Test case post 2",
                visibleLevel=0
            )
        Media.objects.create(
                headline="Test Case image 1",
                category="Test image",
                text="Look at MEEE! I'm Mr MeeCreep",
                cachedText="Look at MEEE! I'm Mr MeeCreep",
                lowResFile="",
                highResFile=""
            )
        Media.objects.create(
                text="Test Case image 2",
                headline="Another test image",
                cachedText="Test Case image 2",
                category="Test image",
                lowResFile="",
                highResFile="")

    def test_total_search(self):
        """
        This should contain all objects through searching
        for Test Case (even case insensitive)
        """
        a1 = Article.objects.get(largeText="Test Case Article 1")
        a2 = Article.objects.get(description="Test Case Article 2")
        a3 = Article.objects.get(description="Test Case Article 3")
        p1 = Post.objects.get(title="Test case post 1")
        p2 = Post.objects.get(cacheText="Test case post 2")
        m1 = Media.objects.get(headline="Test Case image 1")
        m2 = Media.objects.get(text="Test Case image 2")
        res = perform_query_helper("TeSt cAsE", True)
        self.assertTrue(a1 in res)
        self.assertTrue(a3 in res)
        # Delete first occurance of a3 from list to test atomic search result
        res.remove(a3)
        self.assertFalse(a3 in res)
        self.assertFalse(a2 in res)
        self.assertTrue(p1 in res)
        self.assertTrue(p2 in res)
        self.assertTrue(m1 in res)
        self.assertTrue(m2 in res)
        res = perform_query_helper("TeSt cAsE Article", False)
        self.assertTrue(a1 in res)
        self.assertFalse(a2 in res)
        self.assertFalse(a3 in res)
        self.assertFalse(p1 in res)
        self.assertFalse(p2 in res)
        self.assertFalse(m1 in res)
        self.assertFalse(m2 in res)

