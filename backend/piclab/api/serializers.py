from django.utils.timezone import now
from rest_framework import serializers

from .models import Photo, Project


class PhotoSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=False)
    image = serializers.ListField(child=serializers.ImageField(allow_empty_file=False))

    class Meta:
        model = Photo
        fields = [
            'id', 'image', 'name', 'date_created',
            'is_liked', 'project'
        ]

    def create(self, validated_data):
        # Split all images
        images = validated_data.pop('image')
        for image in images:
            # Extract the name from the image and shorten it if necessary
            name = str(image)
            name = name if len(name) < 50 else (name[:48] + '..')
            photo = Photo.objects.create(image=image, name=name, **validated_data)
        return photo
    


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'date_created', 'owner']
        read_only_fields = ['owner']
