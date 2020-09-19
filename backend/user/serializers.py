from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from backend.api.serializers import ProjectSerializer
from .models import Profile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    password_confirm = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )

        password = self.validated_data['password']
        password_confirm = self.validated_data['password_confirm']
        if password != password_confirm:
            raise serializers.ValidationError({'password': 'Passwords must match...'})

        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    projects = ProjectSerializer(source='user.projects', read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'username', 'email', 'projects', 'current_project']
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = User.objects.filter(
                email=request.user.email,
                username=request.user.username,
            ).first()
            instance.user.id = user.id
            project = validated_data.get('current_project')
            if project.owner.id != user.id:
                raise serializers.ValidationError(
                    detail=f'You do not have permission to acess this project ({project.name}).'
                    'Please contact project\'s administrator to request access.')

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance

        raise serializers.ValidationError(
            detail='You are not recognized as a valid user... Please login and try again.')
