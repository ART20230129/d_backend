import os
import mimetypes
import logging
import math
from django.utils.encoding import escape_uri_path
from django.utils.crypto import get_random_string
from django.utils import timezone

from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.http import HttpResponse, Http404, FileResponse
from django.db.models import Count, Sum

from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout, authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from django.core.files.storage import FileSystemStorage
from my_server.models import FileUser
from my_server.permissions import IsOwner
from my_server.serialisers import UserSerializer, UserLoginSerializer, UserListSerializer, FileSerializer, \
    FileListSerializer, UserListUpdateSerializer

logger = logging.getLogger('main_my_cloud_app')

# Регистрация пользователя (user registration)
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                '''создаем токен при регистрации'''
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                logger.info("The user is registered (Пользователь зарегистрирован)")
                return Response(json, status=status.HTTP_201_CREATED)
        logger.error("User registration error (Ошибка регистрации пользователя)")
        return Response({'error': 'Not registered'}, status=status.HTTP_400_BAD_REQUEST)

'''
- Используется UserSerializer, который должен включать поля для имени пользователя, 
пароля и других необходимых данных. Важно, чтобы в сериализаторе была реализована 
логика хеширования пароля перед сохранением в базу данных.
- При получении POST запроса, данные из запроса передаются в сериализатор для валидации. 
Если данные валидны, вызывается метод serializer.save(), который создает нового пользователя.
- В случае успешного создания пользователя, возвращается ответ со статусом 201 Created 
и данными созданного пользователя. В противном случае, возвращается ответ со статусом 400 Bad Request 
и информацией об ошибках валидации.
'''

# Вход пользователя (user login)
@api_view(['POST'])
def login_page(request):
    serializer = UserLoginSerializer(data=request.data)
    try:
        if request.method == "POST":
            user = User.objects.get(username=serializer.initial_data['username'])
            if user is not None:
                user = authenticate(username=serializer.initial_data['username'],
                                    password=serializer.initial_data['password'])
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                logger.info("Authorization was successful (Авторизация прошла успешно)")
                return Response({'message': 'Login successful', 'user_id': user.id, 'token': token.key,
                                 'is_staff': user.is_staff, 'is_superuser': user.is_superuser},
                                status=status.HTTP_200_OK)
    except Exception as e:
            logger.error(str(e))
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )


# Выход пользователя (user output)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        logout(request)
        logger.info('Logout successful (Выход пользователя прошел успешно)')
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    except Exception as e:
            logger.error(str(e))
            return Response({'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

'''
- @api_view(['POST']): Ограничивает view только POST запросами, 
так как выход пользователя обычно инициируется отправкой POST запроса.
- @permission_classes([IsAuthenticated]): Указывает, что только аутентифицированные пользователи 
могут получить доступ к этому view. Это предотвращает выход из системы неавторизованных пользователей.
- logout(request): Функция logout из django.contrib.auth удаляет сессию текущего пользователя.
return Response(...): Возвращает успешный ответ с кодом состояния 200 и сообщением 
об успешном выходе из системы.
'''

class UserUpdateViewSet(ModelViewSet):
    # исключаем из получаемого списка superuser и сортируем полученный список пользователей по id
    queryset = User.objects.all().exclude(is_superuser=True).order_by('id')
    serializer_class = UserListUpdateSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    count_user_files = User.objects.annotate(count_files=Count('files'))

class UserViewSet(APIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get(self, request):
        try:
            # исключаем из получаемого списка superuser и сортируем полученный список пользователей по id
            users = User.objects.all().exclude(is_superuser=True).order_by('id')
            # подсчет количества файлов у каждого пользователя и их суммарный размер
            users_count_files = users.annotate(count_files=Count('files'),
                                               size_files=Sum('files__size_file')
                                               )
            serializer = UserListSerializer(users_count_files, many=True)
            result = serializer.data
            logger.info('The list of users has been successfully generated (Список пользователей успешно сформирован)')
            return Response (result)
        except Exception as e:
            logger.error(str(e))
            return Response({'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

class FileUpload(APIView):
    queryset = FileUser.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            ''' организация фильтрации файлов по их создателю'''
            owner = self.request.user
            ''' пример использования related_name='files' связь многие ко многим
             с сортировкой файлов по дате загрузки на сервер'''
            # вариант сортировки, если в модели не использовать class Meta: ordering = ['-uploaded_at']
            # owner_files = owner.files.all().order_by('-uploaded_at')

            owner_files = owner.files.all()
            ser = FileSerializer(owner_files, many=True)

            ''' вариант отфильтровки файлов конкретного пользователя хранилища'''
            # users_files = FileUser.objects.filter(user=owner)
            # ser = FileSerializer(users_files, many=True)
            logger.info('The list of user files has been received (Получен список файлов пользователя)')
            return Response(ser.data)
        except Exception as e:
            logger.error(str(e))
            return Response({'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request):
        try:
            request_file = request.data['file']
            user = self.request.user
            file_name = request_file.name
            comments = request.data['comments']
            size_file = request_file.size

            '''Генерируем уникальный токен'''
            unique_token = get_random_string(length=32)

            new_file = FileUser(
                user = user,
                file = request_file,
                file_name=file_name,
                comments=comments,
                size_file=size_file,
                file_token= unique_token
            )
            new_file.save()
            logger.info('The file was uploaded successfully (Файл успешно загружен)')
            return Response({'status': 'The file was uploaded successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

class FileView(APIView):
    queryset = FileUser.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    '''функция поиска конкретного файла для удаления/переименования и других действий с ним'''
    def get_object(self,id_file):
        try:
            logger.info('The file you are looking for has been found (Искомый файл найден)')
            return FileUser.objects.get(id=id_file)
        except FileUser.DoesNotExist:
            logger.info('File not found')
            return Response({'message': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id_file):
        try:
            file_del = self.get_object(id_file)
            # file_del = FileUser.objects.filter(id=id_file) # вариант

            '''удаляем физически файл, если он существует в хранилище'''
            if file_del.file and os.path.isfile(file_del.file.path):
                os.remove(file_del.file.path)
            file_del.delete()
            logger.info('The file was deleted successfully (Файл успешно удален)')
            return Response({'status': 'OK. The file was deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def patch(self,request, id_file):
        try:
            file_rename = self.get_object(id_file)
            serializer = FileSerializer(file_rename, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info('The file has been renamed (Файл был переименован)')
                return Response({'status': 'OK. The file has been renamed'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

class AdminFilesManagement(APIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self,request, id_user):
        try:
            owner_files = FileUser.objects.filter(user=id_user)
            ser = FileSerializer(owner_files, many=True)
            logger.info('The list of user files has been received (Получен список файлов пользователя)')
            return Response(ser.data)
        except Exception as e:
            logger.error(str(e))
            return Response({'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, id_user):
        try:
            owner = User.objects.get(id=id_user)
            request_file = request.data['file']
            file_name = request_file.name
            comments = request.data['comments']
            size_file = request_file.size

            '''Генерируем уникальный токен'''
            unique_token = get_random_string(length=32)
            print('unique_token', unique_token)

            new_file = FileUser(
                user = owner,
                file = request_file,
                file_name=file_name,
                comments=comments,
                size_file=size_file,
                file_token= unique_token
            )
            new_file.save()
            logger.info('The file was uploaded successfully (Файл успешно загружен)')
            return Response({'status': 'The file was uploaded successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            return Response({'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_file(request, id_file):
    try:
        file_record = FileUser.objects.get(id=id_file)
        file = file_record.file
        filename = file_record.file_name
        file_record_path = file_record.file.path
        my_content_type, _ = mimetypes.guess_type(file_record_path)
        '''используем timezone.now() иначе будет неверное время последнего скачивания!!!'''
        file_record.last_download = timezone.now()
        file_record.save(update_fields=["last_download"])
        response = HttpResponse(file, content_type= my_content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        logger.info('The file has been downloaded successfully (Файл успешно скачан)')
        return response
    except FileUser.DoesNotExist:
        logger.info('The file has not been downloaded')
        raise Http404("File not found")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_file_link(request, id_file):
    try:
        file_for_link = FileUser.objects.get(id=id_file)
        link = file_for_link.file_token
        logger.info('The file link has been downloaded successfully! (Ссылка на файл успешно загружена!)')
        return Response({'link': link}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(str(e))
        return Response({'message': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def download_file_from_link(request):
    try:
        ''' вычленяем из поступившего запроса link для дальнейшего определения file_token '''
        file_link = request.GET.get('link')

        file_record = FileUser.objects.get(file_token=file_link)
        file = file_record.file
        filename = file_record.file_name
        file_record_path = file_record.file.path
        my_content_type, _ = mimetypes.guess_type(file_record_path)
        file_record.last_download = timezone.now()
        file_record.save(update_fields=["last_download"])
        response = HttpResponse(file, content_type= my_content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        logger.info('The file was successfully downloaded from the link (Файл успешно скачан по ссылке)')
        return response
    except Exception as e:
        logger.error('File not found')
        return Response({'status': 'File not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FileListViewSet(ModelViewSet):
    queryset = FileUser.objects.all()
    serializer_class = FileListSerializer