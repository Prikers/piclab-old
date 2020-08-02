from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from .serializers import RegisterSerializer

User = get_user_model()


class RegisterView(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]  # Otherwise no one can register
    serializer_class = RegisterSerializer