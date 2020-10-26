from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile
from piclab.api.models import Project

User = get_user_model()

# Create a Profile and a default Project after User creation
@receiver(post_save, sender=User)
def create_profile_and_project(sender, instance, created, **kwargs):
    if created:
        project = Project.objects.create(owner=instance, name='Gallery')
        Profile.objects.create(user=instance, current_project=project)

@receiver(post_save, sender=User)
def save_profile_and_project(sender, instance, **kwargs):
    instance.profile.save()
    instance.profile.current_project.save()
