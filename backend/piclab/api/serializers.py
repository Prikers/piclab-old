from django.utils.timezone import now
from rest_framework import serializers

from .models import Photo, Project


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'date', 'is_liked', 'project']

    def create(self, validated_data):
        data = validated_data
        data['name'] = validated_data.get('image')
        data['date'] = now()
        photo = Photo.objects.create(**data)
        return photo


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'date_created', 'owner']
        read_only_fields = ['owner']
