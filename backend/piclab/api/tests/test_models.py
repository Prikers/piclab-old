from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from piclab.api.models import Hash, Photo, Project
from piclab.api.tests.utils import remove_test_images, get_image_file

User = get_user_model()


class TestPhotoModel(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@user.com', username='test', password='poiumlkj')
        self.project = self.user.profile.current_project
        self.image = get_image_file(name='test.jpg')
        self.photo = Photo.objects.create(owner=self.user, project=self.project, image=self.image)

    @classmethod
    def tearDownClass(cls):
        # # Make sure to delete the tmp files after running tests
        remove_test_images()
        # Important: do not forget to call django methods
        super().tearDownClass()

    def test_photo_name_initially_not_set(self):
        self.assertEquals(self.photo.name, '')

    def test_photo_str(self):
        self.assertEquals(
            str(self.photo),
            f'<Photo: {self.photo.name} on {self.photo.datetime_uploaded.strftime("%Y-%m-%d")}>'
        )

    def test_photo_default_values(self):
        self.assertFalse(self.photo.is_liked)
        self.assertEquals(self.photo.datetime_uploaded.date(), date.today())

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
        new_image = get_image_file(name='test_new.jpg', ext='jpeg')
        photo = Photo.objects.create(owner=self.user, project=self.project, image=new_image)
        self.assertEquals(
            photo.image.name,
            f'photos/{self.user.email}/{self.project.id}.{self.project.name}/originals/{new_image.name}'
        )

    def test_photo_thumbnail_upload_path(self):
        thumbnail = get_image_file(name='test_new.jpg', ext='jpeg')
        photo = Photo.objects.create(
            owner=self.user, project=self.project,
            image=self.image, thumbnail=thumbnail,
        )
        self.assertEquals(
            photo.thumbnail.name,
            f'photos/{self.user.email}/{self.project.id}.{self.project.name}/thumbnails/{thumbnail.name}'
        )


class TestProjectModel(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@user.com', username='test', password='poiumlkj')
        # Note: a default project is already created for self.user
        # Let's add another one (so 2 projects are created in total)
        self.project = Project.objects.create(name='test', owner=self.user)
    
    def test_project_str(self):
        self.assertEquals(str(self.project), self.project.name)

    def test_project_default_values(self):
        self.assertEquals(self.project.date_created.date(), date.today())

    def test_project_name_validators(self):
        # Correct values
        project = Project.objects.create(owner=self.user, name='test@-_')
        project.full_clean()
        self.assertEquals(Project.objects.count(), 3)
        # Tool long
        name = 'tes' * 10 + 't'  # 31 characters
        with self.assertRaises(ValidationError):
            project = Project.objects.create(owner=self.user, name=name)
            project.clean_fields()
        # Invalid chararcters
        name = 'test/'
        with self.assertRaises(ValidationError):
            project = Project.objects.create(owner=self.user, name=name)
            project.clean_fields()

    def test_project_access_project_from_user(self):
        new = Project.objects.create(owner=self.user, name='new_test')
        self.assertEquals(self.user.projects.first(), new)

    def test_project_delete_user_cascades(self):
        self.assertEquals(Project.objects.count(), 2)
        self.user.delete()
        self.assertEquals(Project.objects.count(), 0)

    def test_project_query_ordering(self):
        latest_project = Project.objects.create(owner=self.user, name='new_test')
        projects = Project.objects.all()
        self.assertEquals(projects[0], latest_project)

    def test_project_unicity_constraints(self):
        project = Project.objects.first()
        new_user = User.objects.create(
            email='test2@user.com', username='test2', password='poiumlkj')
        # Ok for different users to have the same project name
        Project.objects.create(owner=new_user, name=project.name)
        self.assertEquals(Project.objects.filter(owner=new_user).count(), 2)
        # Not ok for a given user to have the same project name
        with self.assertRaises(IntegrityError):
            Project.objects.create(owner=new_user, name=project.name)


class TestHashModel(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@user.com', username='test', password='poiumlkj')
        self.project = self.user.profile.current_project
        self.image = get_image_file(name='test.jpg')
        self.photo = Photo.objects.create(owner=self.user, project=self.project, image=self.image)
        self.hash = Hash.objects.create(photo=self.photo, hash='11111')

    @classmethod
    def tearDownClass(cls):
        remove_test_images()
        super().tearDownClass()

    def test_hash_str(self):
        self.assertEquals(
            str(self.hash),
            f'< Hash of Photo {self.hash.photo.name}: {self.hash.hash}'
        )

    def test_hash_default_values(self):
        self.assertEquals(self.hash.is_duplicated, False)
        self.assertEquals(self.hash.duplicate_id, None)
        self.assertEquals(self.hash.status, 0)

    def test_hash_access_hash_from_photo(self):
        self.assertEquals(self.photo.hash, self.hash)

    def test_hash_delete_photo_cascades(self):
        self.assertEquals(Hash.objects.count(), 1)
        self.photo.delete()
        self.assertEquals(Hash.objects.count(), 0)

    def test_hash_query_ordering(self):
        self.photo2 = Photo.objects.create(owner=self.user, project=self.project, image=self.image)
        self.photo3 = Photo.objects.create(owner=self.user, project=self.project, image=self.image)
        self.hash2 = Hash.objects.create(photo=self.photo2, hash='22222', status=1)
        self.hash3 = Hash.objects.create(photo=self.photo3, hash='33333')
        hashes = Hash.objects.all()
        self.assertListEqual(
            list(hashes),
            [self.hash2, self.hash3, self.hash]
        )

    def test_hash_status_field(self):
        self.assertListEqual(
            Hash.STATUS,
            [(0, 'no_duplicate'), (1, 'todo'), (2, 'done'), (3, 'skipped')]
        )
