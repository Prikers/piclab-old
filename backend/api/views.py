from django.shortcuts import render
from rest_framework import viewsets

from .models import Photo
from .serializers import PhotoSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all().order_by('-date')
    serializer_class = PhotoSerializer
