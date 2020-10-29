from datetime import date
from pathlib import Path
import shutil

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from piclab.api.models import Photo

User = get_user_model()


class TestPhotoModel(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@user.com', username='test', password='poiumlkj')
        self.project = self.user.profile.current_project
        self.image = SimpleUploadedFile(name='test.jpg',
            content=b'\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01')
        self.photo = Photo.objects.create(owner=self.user, project=self.project, image=self.image)

    @classmethod
    def tearDownClass(cls):
        # Make sure to delete the tmp files after running tests
        from django.conf import settings
        tmp_folder = settings.MEDIA_ROOT
        # Ensure the deleted folder is the expected one
        assert tmp_folder == './tmp-tests'
        # Ensure the tmp folder only contains tmp test images
        tmp_files = [(f.stem, f.suffix) for f in Path(tmp_folder).rglob('*') if f.is_file()]
        assert all([stem.startswith('test') and suffix == '.jpg' for (stem, suffix) in tmp_files])
        # Clean up all files
        shutil.rmtree(tmp_folder, ignore_errors=True)
        # Important: do not forget to call django methods
        super().tearDownClass()

    def test_photo_name_initially_not_set(self):
        self.assertEquals(self.photo.name, '')

    def test_photo_str(self):
        self.assertEquals(
            str(self.photo),
            f'<Photo: {self.photo.name} on {self.photo.date_created.strftime("%Y-%m-%d")}>'
        )

    def test_photo_default_values(self):
        self.assertFalse(self.photo.is_liked)
        self.assertIsNone(self.photo.hash)
        self.assertEquals(self.photo.date_created.date(), date.today())

    def test_photo_access_photo_from_user(self):
        self.assertEquals(self.user.photos.first(), self.photo)

    def test_photo_access_photo_from_project(self):
        self.assertEquals(self.project.photos.first(), self.photo)

    def test_photo_delete_user_cascades(self):
        self.assertEquals(Photo.objects.count(), 1)
        self.user.delete()
        self.assertEquals(Photo.objects.count(), 0)

    def test_photo_delete_project_cascades(self):
        self.assertEquals(Photo.objects.count(), 1)
        self.project.delete()
        self.assertEquals(Photo.objects.count(), 0)

    def test_photo_query_ordering(self):
        latest_photo = Photo.objects.create(owner=self.user, project=self.project, image=self.image)
        photos = Photo.objects.all()
        self.assertEquals(photos[0], latest_photo)

    def test_photo_upload_path(self):
        new_image = SimpleUploadedFile(name='test_new.jpg',
            content=b'\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01')
        photo = Photo.objects.create(owner=self.user, project=self.project, image=new_image)
        self.assertEquals(
            photo.image.name,
            f'photos/{self.user.email}/{self.project.id}.{self.project.name}/originals/{new_image.name}'
        )
