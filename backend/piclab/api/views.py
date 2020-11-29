from django.shortcuts import render
from rest_framework import permissions, viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAdminUser

from .models import Hash, Photo, Project
from .serializers import (
    DetailedHashSerializer, HashSerializer,
    PhotoSerializer, ProjectSerializer
)


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    permission_classes = [IsOwner|IsAdminUser]
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    filter_backends = [SearchFilter]
    search_fields = ['=image']

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
            else:
                Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=response, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied()
        # Get specified project and defaults to user current_project
        project = self.request.query_params.get('project',
            user.profile.current_project.id)
        # Allow admin user to modify any user data (userful for Cloud Functions)
        if user.is_admin:
            owner = Project.objects.get(pk=project).owner
        else:
            owner = user
        return Photo.objects.filter(owner=owner, project=project)


class HashViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    filterset_fields = ['hash', 'is_duplicated']

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':
            return DetailedHashSerializer
        if hasattr(self, 'action') and self.action == 'retrieve':
            return DetailedHashSerializer
        return HashSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise PermissionDenied()
        # Get specified project and defaults to user current_project
        project = self.request.query_params.get('project',
            user.profile.current_project.id)
        # Allow admin user to modify any user data (userful for Cloud Functions)
        if user.is_admin:
            owner = Project.objects.get(pk=project).owner
        else:
            owner = user
        return Hash.objects.filter(photo__owner=owner, photo__project=project)


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
