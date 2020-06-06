from django.shortcuts import render
from rest_framework import viewsets

from .models import Image
from .serializers import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Images to be viewed or edited.
    """
    queryset = Image.objects.all().order_by('-date')
    serializer_class = ImageSerializer
