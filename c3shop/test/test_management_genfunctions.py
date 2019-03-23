from datetime import date

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from frontpage.management.magic import compile_markdown
from frontpage.management import media_actions
from frontpage.models import Profile, Media, MediaUpload

from .init_database import init_db

import os


class TestManagementGenericFunctions(TestCase):
    test_image_path = ""

    def setUp(self):
        # Setup articles for get_article_pcs_free here
        this_dir, this_filename = os.path.split(__file__)
        self.test_image_path = os.path.join(this_dir, "testdata", "cc-test-image.jpg")
        media_actions.PATH_TO_UPLOAD_FOLDER_ON_DISK = ""
        init_db()
        pass

    def test_markdown_generation(self):
        # Only test this thing not throwing exceptions
        self.assertEquals(compile_markdown("# Test MD"),
                          '<h1 id="test-md">Test MD</h1>')

    def test_image_upload(self):
        # since pillow runs unit tests as well we'll simply check for the existance of the images
        p: Profile = Profile.objects.all()[0]
        f = open(self.test_image_path, 'rb')
        img = SimpleUploadedFile(f.name, f.read(), content_type="image/jpg")
        media_actions.handle_file(p, "A Test image headline", "Silly Test Images",
                                  "This is a more detailed description of a CC test image", img)
        assumed_path_hr = "uploads/" + str(date.today().year) + "/HIGHRES_cc-test-image.jpg"
        assumed_path_lr = "uploads/" + str(date.today().year) + "/LOWRES_cc-test-image.jpg"
        self.assertTrue(os.path.isfile(assumed_path_hr))
        self.assertTrue(os.path.isfile(assumed_path_lr))
        self.assertTrue(os.path.getsize(assumed_path_hr) > os.path.getsize(assumed_path_lr))
        med_obj: Media = Media.objects.all()[0]
        self.assertEquals(med_obj.headline, "A Test image headline")
        self.assertEquals(med_obj.category, "Silly Test Images")
        self.assertEquals(med_obj.text, "This is a more detailed description of a CC test image")
        self.assertEquals(med_obj.cachedText,
                          compile_markdown("This is a more detailed description of a CC test image"))
        self.assertEquals(med_obj.lowResFile, "/" + assumed_path_lr)
        self.assertEquals(med_obj.highResFile, "/" + assumed_path_hr)
        self.assertEquals(MediaUpload.objects.get(MID=med_obj).UID, p)
        # Clean up FS
        os.remove(assumed_path_lr)
        os.remove(assumed_path_hr)
        if not os.listdir("uploads/" + str(date.today().year)):
            os.rmdir("uploads/" + str(date.today().year))
        if not os.listdir("uploads"):
            os.rmdir("uploads")
        pass
