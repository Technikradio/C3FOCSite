from django.test import TestCase
from frontpage.management.magic import compile_markdown

class TestManagementGenericFunctions(TestCase):
    def setUp(self):
        # Setup articles for get_article_pcs_free here
        pass


    def test_markdown_generation(self):
        # Only test this thing not throwing exceptions
        self.assertEquals(compile_markdown("# Test MD"),
                '<h1 id="test-md">Test MD</h1>')

