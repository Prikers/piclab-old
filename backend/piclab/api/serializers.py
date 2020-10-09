from django.utils.timezone import now
from rest_framework import serializers

from .models import Photo, Project


class PhotoSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=False)

    class Meta:
        model = Photo
        fields = [
            'id', 'image', 'name', 'date_created',
            'is_liked', 'project'
        ]

    def create(self, validated_data):
        name = str(validated_data.get('image'))
        name = name if len(name) < 40 else (name[:37] + '...')
        photo = Photo.objects.create(name=name, **validated_data)
        return photo


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'date_created', 'owner']
        read_only_fields = ['owner']
