from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.test import APIClient

from piclab.api.models import Hash, Photo, Project
from piclab.api.views import FilterHashView, HashViewSet, PhotoViewSet, ProjectViewSet, IsOwner
from piclab.api.serializers import DetailedHashSerializer, HashSerializer, PhotoSerializer, ProjectSerializer
from piclab.api.tests.utils import get_image_file, remove_test_images

User = get_user_model()


class TestProjectViews(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', email='test@user.com', password='poiumlkj')
        self.project = self.user.profile.current_project
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_project_viewset_structure(self):
        self.assertEquals(ProjectViewSet.serializer_class, ProjectSerializer)
        self.assertTupleEqual(ProjectViewSet.permission_classes, (IsOwner,))

    def test_project_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('Project-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_get_list(self):
        Project.objects.create(name='Gallery2', owner=self.user)
        projects = Project.objects.all()
        url = reverse('Project-list')
        response = self.client.get(url)
        serializer = ProjectSerializer(projects, many=True)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_project_get_detail(self):
        url = reverse('Project-detail', args=[self.project.id])
        response = self.client.get(url)
        serializer = ProjectSerializer(self.project)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_project_post(self):
        url = reverse('Project-list')
        response = self.client.post(url, data={'name': 'test'})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset({'name': 'test', 'owner': self.user.id}, response.data)

    def test_project_delete(self):
        url = reverse('Project-detail', args=[self.project.id])
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Project.objects.count(), 0)

    def test_project_update(self):
        url = reverse('Project-detail', args=[self.project.id])
        response = self.client.patch(url, data={'name': 'Gallery_updated'})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Project.objects.first().name, 'Gallery_updated')


class TestPhotoViews(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', email='test@user.com', password='poiumlkj')
        self.project = self.user.profile.current_project
        self.image = get_image_file(name='test.jpg')
        self.photo = Photo.objects.create(owner=self.user, project=self.project, image=self.image)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @classmethod
    def tearDownClass(cls):
        remove_test_images()
        super().tearDownClass()

    def test_photo_viewset_structure(self):
        self.assertEquals(PhotoViewSet.serializer_class, PhotoSerializer)

    def test_photo_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('Photo-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_photo_get_list(self):
        Photo.objects.create(owner=self.user, project=self.project, image=self.image)
        photos = Photo.objects.all()
        url = reverse('Photo-list')
        response = self.client.get(url)
        serializer = PhotoSerializer(photos, many=True)
        for item in response.data:
            item['image'] = item['image'].replace('http://testserver', '')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_photo_get_detail(self):
        url = reverse('Photo-detail', args=[self.photo.id])
        response = self.client.get(url)
        serializer = PhotoSerializer(self.photo)
        response.data['image'] = response.data['image'].replace('http://testserver', '')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_photo_post(self):
        image = get_image_file('other.jpg')
        url = reverse('Photo-list')
        response = self.client.post(url, data={'project': self.project.id}, files=[('image', image.file)], format='multipart')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_photo_delete(self):
        # Note: project will default to user current project
        url = reverse('Photo-detail', args=[self.photo.id])
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Photo.objects.count(), 0)

    def test_photo_update(self):
        url = reverse('Photo-detail', args=[self.photo.id])
        response = self.client.patch(url, data={'is_liked': True})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Photo.objects.first().is_liked, True)

    def test_photo_admin_user_can_update_any_photo(self):
        admin = User.objects.create_superuser(username='admin', email='admin@user.com', password='poiumlkj')
        self.client.force_authenticate(user=admin)
        url = reverse('Photo-detail', args=[self.photo.id]) + f'?project={self.project.id}'
        response = self.client.patch(url, data={'is_liked': True})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Photo.objects.first().is_liked, True)


class TestHashView(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', email='test@user.com', password='poiumlkj')
        self.admin_user = User.objects.create_superuser(
            username='testAdmin', email='testAdmin@user.com', password='poiumlkj')
        self.project = self.user.profile.current_project
        self.image = get_image_file()
        self.photo = Photo.objects.create(owner=self.user, project=self.project, image=self.image)
        self.hash = Hash.objects.create(
            hash='afe43346cd3e543', is_duplicated=False, status=0, photo=self.photo)
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

    @classmethod
    def tearDownClass(cls):
        remove_test_images()
        super().tearDownClass()

    def test_hash_viewset_structure(self):
        # Serializer class is tested separately
        self.assertTupleEqual(HashViewSet.permission_classes, (IsAdminUser,))
        self.assertEquals(HashViewSet.filterset_class, FilterHashView)

    def test_hash_get_serializer_class(self):
        viewset = HashViewSet()
        self.assertEquals(viewset.get_serializer_class(), HashSerializer)
        viewset.action = 'list'
        self.assertEquals(viewset.get_serializer_class(), DetailedHashSerializer)
        viewset.action = 'retrieve'
        self.assertEquals(viewset.get_serializer_class(), DetailedHashSerializer)

    def test_hash_only_admin_users(self):
        url = reverse('Hash-list')
        # No User
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # A non-admin user
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_hash_get_list(self):
        other_photo = Photo.objects.create(owner=self.user, project=self.project, image=self.image)
        Hash.objects.create(hash='xxx', is_duplicated=False, status=0, photo=other_photo)
        hashes = Hash.objects.all()

        url = reverse('Hash-list')
        response = self.client.get(url, data={'project': self.project.id})
        for item in response.data:
            item['photo']['image'] = item['photo']['image'].replace('http://testserver', '')

        serializer = DetailedHashSerializer(hashes, many=True)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_hash_get_detail(self):
        url = reverse('Hash-detail', args=[self.hash.id])
        response = self.client.get(url, data={'project': self.project.id})
        serializer = DetailedHashSerializer(self.hash)
        response.data['photo']['image'] = response.data['photo']['image'].replace('http://testserver', '')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_hash_post(self):
        other_photo = Photo.objects.create(owner=self.user, project=self.project, image=self.image)
        data = {'photo': other_photo.id, 'hash': 'superhash'}
        url = reverse('Hash-list')
        response = self.client.post(url, data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_hash_delete(self):
        url = reverse('Hash-detail', args=[self.hash.id]) + f'?project={self.project.id}'
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Hash.objects.count(), 0)

    def test_hash_update(self):
        self.assertEquals(Hash.objects.first().is_duplicated, False)
        url = reverse('Hash-detail', args=[self.hash.id]) + f'?project={self.project.id}'
        response = self.client.patch(url, data={'is_duplicated': True})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Hash.objects.first().is_duplicated, True)
