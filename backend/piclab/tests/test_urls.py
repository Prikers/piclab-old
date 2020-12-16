from django.test import SimpleTestCase
from django.urls import resolve, reverse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from piclab.user.views import RegisterView, ProfileViewSet
from piclab.api.views import HashViewSet, PhotoViewSet, ProjectViewSet


class TestUrls(SimpleTestCase):

    def test_api_token_resolves(self):
        url = reverse('token_obtain_pair')
        self.assertEquals(url, '/api/token/')
        self.assertEquals(resolve(url).func.view_class, TokenObtainPairView)

    def test_api_token_refresh_resolves(self):
        url = reverse('token_refresh')
        self.assertEquals(url, '/api/token/refresh/')
        self.assertEquals(resolve(url).func.view_class, TokenRefreshView)

    def test_api_token_verify_resolves(self):
        url = reverse('token_verify')
        self.assertEquals(url, '/api/token/verify/')
        self.assertEquals(resolve(url).func.view_class, TokenVerifyView)

    def test_api_register_resolves(self):
        url = reverse('register')
        self.assertEquals(url, '/api/register/')
        self.assertEquals(resolve(url).func.view_class, RegisterView)

    def test_api_router_photos_resolves(self):
        url = reverse('Photo-list')
        self.assertEquals(url, '/api/photos/')
        self.assertEquals(resolve(url).func.cls, PhotoViewSet)

    def test_api_router_photos_details_resolves(self):
        url = reverse('Photo-detail', args=[1])
        self.assertEquals(url, '/api/photos/1/')
        self.assertEquals(resolve(url).func.cls, PhotoViewSet)

    def test_api_router_projects_resolves(self):
        url = reverse('Project-list')
        self.assertEquals(url, '/api/projects/')
        self.assertEquals(resolve(url).func.cls, ProjectViewSet)

    def test_api_router_projects_details_resolves(self):
        url = reverse('Project-detail', args=[1])
        self.assertEquals(url, '/api/projects/1/')
        self.assertEquals(resolve(url).func.cls, ProjectViewSet)

    def test_api_router_profiles_resolves(self):
        url = reverse('Profile-list')
        self.assertEquals(url, '/api/profile/')
        self.assertEquals(resolve(url).func.cls, ProfileViewSet)

    def test_api_router_profiles_details_resolves(self):
        url = reverse('Profile-detail', args=[1])
        self.assertEquals(url, '/api/profile/1/')
        self.assertEquals(resolve(url).func.cls, ProfileViewSet)

    def test_api_router_hashes_resolves(self):
        url = reverse('Hash-list')
        self.assertEquals(url, '/api/hash/')
        self.assertEquals(resolve(url).func.cls, HashViewSet)

    def test_api_router_hashes_details_resolves(self):
        url = reverse('Hash-detail', args=[1])
        self.assertEquals(url, '/api/hash/1/')
        self.assertEquals(resolve(url).func.cls, HashViewSet)
