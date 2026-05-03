
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from django.conf import settings
from django.conf.urls.static import static

from my_server.views import logout_view, UserViewSet, login_page, RegisterView, \
    FileUpload, FileView, download_file, download_file_link, download_file_from_link, UserUpdateViewSet, AdminFilesManagement

router = DefaultRouter()
router.register('users', UserUpdateViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logout_view, name='logout'),
    path('uploadfile/', FileUpload.as_view()),
    path('deletefile/<int:id_file>/', FileView.as_view()),
    path('renamefile/<int:id_file>/', FileView.as_view()),
    path('downloadfile/<int:id_file>/', download_file),
    path('downloadlinkfile/<int:id_file>/', download_file_link),
    path('downloadfilefromlink/', download_file_from_link),
    path('users/', UserViewSet.as_view()),
    path('users/<int:id_user>/', UserViewSet.as_view()),
    path('uploadfileuser/<int:id_user>/', AdminFilesManagement.as_view()),

]

'''
Django по умолчанию не обслуживает медиа в режиме разработки.
Это нужно настроить явно в главном файле urls.py:
'''
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
Условие if settings.DEBUG критически важно — в продакшене статические файлы 
должен обслуживать веб-сервер (Nginx, Apache), а не Django.
'''
