from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory

from piclab.api.models import Project
from piclab.user.models import Profile
from piclab.user.serializers import RegisterSerializer, ProfileSerializer

User = get_user_model()


class TestRegisterSerializer(TestCase):

    def setUp(self):
        self.data = {
            'email': 'test@user.com',
            'username': 'test',
            'password': 'poiumlkj',
            'password_confirm': 'poiumlkj',
        }
        self.serializer = RegisterSerializer(data=self.data)
        self.serializer.is_valid()

    def test_user_structure(self):
        self.assertEquals(RegisterSerializer.Meta.model, User)
        self.assertDictEqual(RegisterSerializer.Meta.extra_kwargs,
                             {'password': {'write_only': True}})
    
    def test_user_contains_expected_fields(self):
        self.assertListEqual(
            list(self.serializer.data.keys()),
            ['email', 'username'],
        )
        self.assertEquals(self.serializer.data['email'], self.data['email'])
        self.assertEquals(self.serializer.data['username'], self.data['username'])

    def test_user_save_sets_password(self):
        self.assertIsNone(User.objects.first())
        self.serializer.save()
        self.assertEquals(User.objects.count(), 1)
        self.assertTrue(User.objects.first().has_usable_password())

    def test_user_unvalid_password_confirm(self):
        self.data['password_confirm'] = 'wrong'
        serializer = RegisterSerializer(data=self.data)
        serializer.is_valid()
        with self.assertRaises(ValidationError):
            serializer.save()


class TestProfileSerializer(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@user.com', username='test', password='poiumlkj')
        self.profile = self.user.profile
        self.project = self.user.profile.current_project
        self.serializer = ProfileSerializer(instance=self.profile)

    def test_profile_structure(self):
        self.assertEquals(ProfileSerializer.Meta.model, Profile)

    def test_profile_contains_expected_fields(self):
        self.assertListEqual(
            list(self.serializer.data.keys()),
            ['id', 'user', 'username', 'email', 'projects', 'current_project'],
        )

    def test_profile_update_current_project_bad_authentication(self):
        self.assertEquals(self.user.profile.current_project, self.project)
        other_user = User.objects.create(email='test2@user.com', username='test2', password='poiumlkj')
        other_project = Project.objects.create(name='test', owner=other_user)
        with self.assertRaises(ValidationError):
            self.serializer.update(self.profile, {'current_project': other_project})

    def test_profile_update_current_project(self):
        # Current project is self.project
        self.assertEquals(self.user.profile.current_project, self.project)
        # Authenticate the request
        request = APIRequestFactory().get('/')
        request.user = self.user
        # Create a new project and update current_project
        new_project = Project.objects.create(name='test', owner=self.user)
        serializer = ProfileSerializer(instance=self.profile, context={'request': request})
        serializer.update(self.profile, validated_data={'current_project': new_project})
        # Current project is now new_project
        self.assertEquals(self.user.profile.current_project, new_project)
