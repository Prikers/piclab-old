from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView

from .serializers import RegisterSerializer, ProfileSerializer
from .models import Profile

User = get_user_model()


class RegisterView(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]  # Otherwise no one can register
    serializer_class = RegisterSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    model = Profile
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Profile.objects.filter(user=user)
        raise PermissionDenied()
