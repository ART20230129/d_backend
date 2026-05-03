from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from my_server.models import FileUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password']) # хешируем пароль
        return User.objects.create(**validated_data)



'''Обратите внимание на использование make_password 
для хеширования пароля при создании нового пользователя.'''

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserListSerializer(serializers.ModelSerializer):
    count_files = serializers.IntegerField()
    size_files = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'count_files', 'size_files' ]
        ordering = ['id']

class UserListUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff' ]
        ordering = ['id']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUser
        fields = ['id', 'user', 'file', 'file_name', 'comments', 'size_file', 'uploaded_at', 'last_download']
        read_only_fields = ['user']

class FileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUser
        fields = ['id', 'user', 'file', 'file_name', 'comments', 'size_file', 'uploaded_at', 'last_download']