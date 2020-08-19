from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from .models import Photo, Project
from .serializers import PhotoSerializer, ProjectSerializer


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    permission_classes = (IsOwner,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        print(self.request.query_params)
        print(self.request.data)
        if user.is_authenticated:
            return Photo.objects.filter(owner=user)
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
