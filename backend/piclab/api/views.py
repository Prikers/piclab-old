from django.shortcuts import render
from rest_framework import permissions, viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Photo, Project
from .serializers import PhotoSerializer, ProjectSerializer


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    permission_classes = (IsOwner,)
    parser_classes = (MultiPartParser, FormParser, JSONParser,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def create(self, request, *args, **kwargs):
        images = request.data.getlist('image')
        data = request.data
        response = []
        for image in images:
            data['image'] = image
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                self.perform_create(serializer)
                response.append(serializer.data)
        return Response(data=response, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        project = self.request.query_params.get('project')
        if user.is_authenticated:
            return Photo.objects.filter(owner=user, project=project)
        raise PermissionDenied()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = (IsOwner,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Project.objects.filter(owner=user)
        raise PermissionDenied()
