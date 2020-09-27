from rest_framework import serializers

from .models import Photo, Project


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'src', 'name', 'date', 'is_liked', 'project']


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'date_created', 'owner']
        read_only_fields = ['owner']
