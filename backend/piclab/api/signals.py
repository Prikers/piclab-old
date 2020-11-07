from pathlib import Path

from django.core.files.storage import default_storage
from django.db.models.signals import post_delete
from django.dispatch import receiver

from piclab.api.models import Photo


@receiver(post_delete, sender=Photo)
def remove_file_from_storage(sender, instance, using, **kwargs):
    if instance.image:
        try:
            path = Path(instance.image.name)
            thumbnail = str(path.parent.parent / 'thumbnails' / path.name)
            instance.image.delete(save=False)
            default_storage.delete(thumbnail)
        except Exception as e:
            pass
