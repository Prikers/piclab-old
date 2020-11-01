from pathlib import Path

from django.utils.timezone import now
from rest_framework import serializers

from .models import Photo, Project


class PhotoSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=False)

    class Meta:
        model = Photo
        fields = [
            'id', 'image', 'name', 'date_created',
            'is_liked', 'project', 'hash',
        ]

    def create(self, validated_data):
        name = Path(str(validated_data.get('image')))
        stem, suffix = name.stem, name.suffix
        name = name if len(stem) < 40 else (f'{stem[:37]}_{suffix}')
        photo = Photo.objects.create(name=name, **validated_data)
        return photo


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'date_created', 'owner']
        read_only_fields = ['owner']
