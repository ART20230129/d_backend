from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import truncatechars

# Create your models here.

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class FileUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=user_directory_path, null=True)
    file_name = models.CharField(max_length=255, null=True)
    comments = models.TextField(null=True, blank=True)
    size_file = models.BigIntegerField(null=True,  blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_download = models.DateTimeField(null=True, blank=True)
    file_token = models.CharField(max_length=32, null=True, blank=True)

    # вывод не более 20 символов комментария, через аминку почему-то не работает
    @property
    def comment_short_description(self):
        if len(self.comments) > 20:
            return truncatechars(self.comments, 20)
        return (self.comments)

    class Meta:
        ordering = ['-uploaded_at']
