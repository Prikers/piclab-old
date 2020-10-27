from django.test import TestCase
from django.contrib.auth import get_user_model

from piclab.user.models import Profile
from piclab.api.models import Project

User = get_user_model()


class TestSignals(TestCase):

    def test_signal_creates_profile(self):
        user = User.objects.create_user(email='test@user.com', username='test', password='poiumlkj')
        self.assertEquals(Profile.objects.count(), 1)
        self.assertEquals(Profile.objects.first().user, user)

    def test_signal_creates_default_project(self):
        user = User.objects.create_user(email='test@user.com', username='test', password='poiumlkj')
        self.assertEquals(Project.objects.count(), 1)
        self.assertEquals(Project.objects.first().owner, user)
        self.assertEquals(Project.objects.first().name, 'Gallery')

    def test_signal_add_current_project(self):
        User.objects.create_user(email='test@user.com', username='test', password='poiumlkj')
        project = Project.objects.first()
        profile = Profile.objects.first()
        self.assertEquals(profile.current_project, project)
