from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.test import APIClient
from piclab.user.models import Profile

from piclab.api.models import Project
from piclab.user.views import RegisterView, ProfileViewSet
from piclab.user.serializers import RegisterSerializer, ProfileSerializer

User = get_user_model()


class TestRegisterView(TestCase):

    def test_register_createview_structure(self):
        self.assertEquals(RegisterView.serializer_class, RegisterSerializer)
        self.assertEquals(RegisterView.permission_classes, [AllowAny])
        self.assertEquals(RegisterView.model, User)

    def test_register_create_user(self):
        url = reverse('register')
        response = APIClient().post(url, {
            'username': 'test', 'email': 'test@user.com',
            'password': 'poiumlkj', 'password_confirm': 'poiumlkj'
        })
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(User.objects.count(), 1)
        self.assertEquals(User.objects.first().username, 'test')

    def test_register_create_user_invalid_passwords(self):
        url = reverse('register')
        response = APIClient().post(url, {
            'username': 'test', 'email': 'test@user.com',
            'password': 'poiumlkj', 'password_confirm': 'not_valid'
        })
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(User.objects.count(), 0)


class TestProfileViews(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', email='test@user.com', password='poiumlkj')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_profile_viewset_structure(self):
        self.assertEquals(ProfileViewSet.serializer_class, ProfileSerializer)
        self.assertEquals(ProfileViewSet.permission_classes, [IsAuthenticated])
        self.assertEquals(ProfileViewSet.model, Profile)

    def test_profile_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('Profile-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_get_list(self):
        url = reverse('Profile-list')
        response = self.client.get(url)
        serializer = ProfileSerializer([self.user.profile], many=True)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_profile_get_only_user_profiles(self):
        User.objects.create(username='other', email='other@user.com', password='poiumlkj')
        url = reverse('Profile-list')
        response = self.client.get(url)
        serializer = ProfileSerializer([self.user.profile], many=True)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Profile.objects.count(), 2)
        self.assertEquals(response.data, serializer.data)

    def test_profile_get_detail(self):
        url = reverse('Profile-detail', args=[self.user.profile.id])
        response = self.client.get(url)
        serializer = ProfileSerializer(self.user.profile)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_profile_update(self):
        other_project = Project.objects.create(owner=self.user, name='Other')
        url = reverse('Profile-detail', args=[self.user.profile.id])
        response = self.client.patch(url, data={'current_project': other_project.id})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Profile.objects.first().current_project, other_project)
