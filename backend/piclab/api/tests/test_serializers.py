from django.contrib.auth import get_user_model
from django.test import TestCase

from piclab.api.models import Hash, Photo, Project
from piclab.api.serializers import DetailedHashSerializer, HashSerializer, PhotoSerializer, ProjectSerializer
from piclab.api.tests.utils import remove_test_images, get_image_file

User = get_user_model()


class TestProjectSerializer(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@user.com', username='test', password='poiumlkj')
        self.data = {
            'owner': self.user,
            'name': 'test',
        }
        self.project = Project(**self.data)
        self.serializer = ProjectSerializer(instance=self.project)

    def test_project_structure(self):
        self.assertEquals(ProjectSerializer.Meta.model, Project)
        self.assertIn('owner', ProjectSerializer.Meta.read_only_fields)

    def test_project_contains_expected_fields(self):
        self.assertListEqual(
            list(self.serializer.data.keys()),
            ['id', 'name', 'date_created', 'owner'],
        )

    def test_project_fields_content(self):
        self.assertEquals(self.serializer.data['name'], self.data['name'])
        self.assertEquals(self.serializer.data['owner'], self.data['owner'].id)
        self.assertEquals(self.serializer.data['id'], self.project.id)

    def test_project_invalid_name(self):
        data = self.data
        # Invalid characters
        data['name'] = 'test/'
        serializer = ProjectSerializer(instance=self.project, data=data)
        self.assertFalse(serializer.is_valid())
        # Too long
        data['name'] = 'tes' * 10 +'t'  # 31 characters
        serializer = ProjectSerializer(instance=self.project, data=data)
        self.assertFalse(serializer.is_valid())


class TestPhotoSerializer(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@user.com', username='test', password='poiumlkj')
        self.project = self.user.profile.current_project
        self.image = get_image_file()
        self.photo = Photo.objects.create(owner=self.user, project=self.project, image=self.image)
        self.serializer = PhotoSerializer(instance=self.photo)

    @classmethod
    def tearDownClass(cls):
        remove_test_images()
        super().tearDownClass()

    def test_photo_structure(self):
        self.assertEquals(PhotoSerializer.Meta.model, Photo)

    def test_photo_contains_expected_fields(self):
        self.assertListEqual(
            list(self.serializer.data.keys()),
            ['id', 'image', 'name', 'thumbnail', 'datetime_uploaded', 'project',
            'datetime_photo', 'file_size', 'width', 'height', 'dpi',
            'camera', 'longitude', 'latitude', 'exif', 'hash_id', 'is_liked'],
        )

    def test_photo_name_is_added(self):
        name = 'test.jpg'
        image = get_image_file(name=name)
        data = {
            'project': self.project.id,
            'image': image
        }
        serializer = PhotoSerializer(data=data)
        serializer.is_valid()
        serializer.save(owner=self.user)
        self.assertEquals(serializer.data['name'], name)

    def test_photo_name_too_long(self):
        name = 'test' * 10 + '.jpg'
        shortened = ('test' * 10)[:37] + '_' + '.jpg'
        image = get_image_file(name=name)
        data = {
            'project': self.project.id,
            'image': image
        }
        serializer = PhotoSerializer(data=data)
        serializer.is_valid()
        serializer.save(owner=self.user)
        self.assertEquals(serializer.data['name'], shortened)


class TestHashSerialized(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@user.com', username='test', password='poiumlkj')
        self.project = self.user.profile.current_project
        self.image = get_image_file()
        self.photo = Photo.objects.create(owner=self.user, project=self.project, image=self.image)
        self.hash = Hash.objects.create(
            hash='afe43346cd3e543', is_duplicated=False, status=0, photo=self.photo)

    @classmethod
    def tearDownClass(cls):
        remove_test_images()
        super().tearDownClass()

    def test_hash_structure(self):
        self.assertEquals(HashSerializer.Meta.model, Hash)

    def test_hash_contains_expected_fields(self):
        serializer = HashSerializer(instance=self.hash)
        self.assertListEqual(
            list(serializer.data.keys()),
            ['id', 'photo', 'hash', 'is_duplicated',
            'duplicate_id', 'status', 'date_status'],
        )
        self.assertIsInstance(serializer.data['photo'], int)

    def test_hash_detailed_contains_expected_fields(self):
        serializer = DetailedHashSerializer(instance=self.hash)
        self.assertListEqual(
            list(serializer.data.keys()),
            ['id', 'photo', 'hash', 'is_duplicated',
            'duplicate_id', 'status', 'date_status',]
        )
        self.assertIsInstance(serializer.data['photo'], dict)
