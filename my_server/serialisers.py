import re
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from my_server.models import FileUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9]{3,19}$', value):
            raise serializers.ValidationError(
                'Логин должен быть от 4 до 20 символов, начинаться с буквы, содержать только латиницу и цифры')
        return value

    def validate_password(self, value):
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{6,}$', value):
            raise serializers.ValidationError(
                'Пароль должен содержать минимум 6 символов, одну заглавную букву, одну цифру и один спец. символ.'
            )
        return value

    def validate_email(self, value):
        if not re.match(r'^(.+)@(.+)\.(.+)$', value):
            raise serializers.ValidationError(
                'Неверный формат email.'
            )
        return value

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