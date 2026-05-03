from django.contrib import admin
from my_server.models import FileUser


@admin.register(FileUser)
class FileUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_name', 'comment_short_description', 'size_file', 'uploaded_at', 'last_download')

    # @admin.display() #  не работает
    # def comments(self, obj) -> str:
    #     print(len(obj.comments))
    #     if len(obj.comments) > 20:
    #         return f'{obj.comments[:17]}...'
    #     return obj.comments[20]

