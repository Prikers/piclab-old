from pathlib import Path

from django.core.files.storage import default_storage
from django.db.models.signals import post_delete
from django.dispatch import receiver

from piclab.api.models import Photo


@receiver(post_delete, sender=Photo)
def remove_file_from_storage(sender, instance, using, **kwargs):
    if instance.image:
        try:
            instance.image.delete(save=False)
            instance.thumbnail.delete(save=False)
        except Exception as e:
            pass
