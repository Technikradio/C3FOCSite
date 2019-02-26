import os
import logging

from django.test import TestCase
from frontpage.management.messages import load_in_data, get_message, logger

class TestMessageSystem(TestCase):

    TEST_MESSAGES_FILE = ""

    def setUp(self):
        # Load in test data
        this_dir, this_filename = os.path.split(__file__)
        self.TEST_MESSAGES_FILE = os.path.join(this_dir, "testdata", "test_messages.csv")
        load_in_data(self.TEST_MESSAGES_FILE)
        logger.setLevel(logging.CRITICAL) #  make sure to not bloat the
        #  output if everything is fine.

    def test_message_reading(self):
        self.assertEquals(get_message("1;test"), "This is a test")
        self.assertEquals(get_message("2;test\\; Sherlock."), "This is also a test; Sherlock.")
        self.assertEquals(get_message("3"), "The requested message (3) wasn't found")

