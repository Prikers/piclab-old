from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils import timezone

User = get_user_model()

ERROR_REGEX_PROJECT = 'Enter a valid project name. This value may only contain letters, numbers or one of the following characters: @, -, _'


class Project(models.Model):

    name = models.CharField(max_length=30, validators=[
        RegexValidator(regex='^[\w.@+\-]+$', message=ERROR_REGEX_PROJECT)
    ])
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    date_created = models.DateTimeField(verbose_name='date created', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_created']
        constraints = [
            models.UniqueConstraint(fields=['owner', 'name'], name='unique_name_per_user')
        ]


def upload_path(instance, filename):
    folder = 'photos'
    return f'{folder}/{instance.owner.email}/{instance.project.id}.{instance.project.name}/originals/{filename}'

def upload_path_thumbnail(instance, filename):
    return upload_path(instance, filename).replace('originals', 'thumbnails')


class Photo(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='photos')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=upload_path)
    thumbnail = models.ImageField(upload_to=upload_path_thumbnail, null=True, blank=True)
    name = models.CharField(max_length=50)
    datetime_uploaded = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    # Metadata fields
    datetime_photo = models.DateTimeField(null=True, blank=True)
    file_size = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    dpi = models.CharField(null=True, blank=True, max_length=50)
    camera = models.CharField(null=True, blank=True, max_length=100)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    exif = models.JSONField(null=True, default=dict)
    # User inputs fields
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f'<Photo: {self.name} on {self.datetime_uploaded.strftime("%Y-%m-%d")}>'

    class Meta:
        ordering = ['-datetime_uploaded']


class Hash(models.Model):

    NO_DUPLICATE = 0
    TODO = 1
    DONE = 2
    SKIPPED = 3
    STATUS = [
        (NO_DUPLICATE, 'no_duplicate'),
        (TODO, 'todo'),
        (DONE, 'done'),
        (SKIPPED, 'skipped'),
    ]

    photo = models.OneToOneField(Photo, on_delete=models.CASCADE)
    hash = models.CharField(max_length=256, null=True, blank=True)
    is_duplicated = models.BooleanField(default=False)
    duplicate_id = models.CharField(max_length=128, null=True, default=None)
    status = models.SmallIntegerField(choices=STATUS, default=NO_DUPLICATE)
    date_status = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return f'< Hash of Photo {self.photo.name}: {self.hash}'

    class Meta:
        ordering = ['-status', '-date_status']
