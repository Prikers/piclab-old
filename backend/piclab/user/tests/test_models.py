from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import DataError, IntegrityError
from django.test import TestCase

from piclab.user.models import Profile

User = get_user_model()


class TestUserManager(TestCase):

    def test_create_valid_user(self):
        user = User.objects.create_user(
            email='test@user.com', username='test', password='test')
        self.assertEquals(user.email, 'test@user.com')
        self.assertEquals(user.username, 'test')
    
    def test_create_invalid_user(self):
        # Missing email
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username='test', password='test',
            )
        # Missing username
        with self.assertRaises(TypeError):
            User.objects.create_user(
                email='test@user.com', password='test',
            )

    def test_create_valid_superuser(self):
        superuser = User.objects.create_superuser(
            email='test@user.com', username='test')
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class TestUserModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@user.com', username='test')

    def test_user_model_structure(self):
        # Validate it uses correct User Manager
        self.assertTrue(isinstance(self.user, User))
        # Validate the required fields and username fields
        self.assertEquals(self.user.USERNAME_FIELD, 'email')
        self.assertListEqual(self.user.REQUIRED_FIELDS, ['username'])

    def test_user_str(self):
        self.assertEquals(str(self.user), '<User: test, Email: test@user.com>')

    def test_user_default_attributes(self):
        self.assertFalse(self.user.is_admin)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertEquals(self.user.date_joined.date(), date.today())

    def test_user_username_length_validators(self):
        # Too short
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email='test1@user.com', username='te', password='poiumlkj'
                ).clean_fields()
        # Too long
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email='test2@user.com', username='test'*10, password='poiumlkj'
                ).clean_fields()

    def test_user_username_characters_validators(self):
        # Invalid special characters
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email='test1@user.com', username='test#', password='poiumlkj'
                ).clean_fields()
        # Valid special characters
        user = User.objects.create_user(
            email='test2@user.com', username='test@.+-_', password='poiumlkj'
        )
        user.full_clean()
        self.assertTrue(user.is_active)

    def test_user_email_validators(self):
        # Not a valid email
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email='notanemail', username='test1', password='poiumlkj'
                ).clean_fields()
        # Too long
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email='test'*25+'@user.com', username='test2', password='poiumlkj'
                ).clean_fields()

    def test_user_username_unicity(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='test1@user.com', username='test', password='poiumlkj')

    def test_user_email_unicity(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='test@user.com', username='test1', password='poiumlkj')

    def cleanUp(self):
        self.user.delete()


class TestProfileModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@user.com', username='test', password='poiumlkj'
        )
    
    def test_user_has_profile(self):
        self.assertEquals(Profile.objects.count(), 1)
        self.assertEquals(Profile.objects.first().user, self.user)
    
    def test_profile_str(self):
        profile = Profile.objects.first()
        self.assertEquals(str(profile), f'Profile of {self.user.username}')
