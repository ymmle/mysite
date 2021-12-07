from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.fields import exceptions


# Create your models here.
class RequireType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Require(models.Model):
    title = models.CharField(max_length=50)
    require_type = models.ForeignKey(RequireType, on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    JIRA_Testcase_ID = models.CharField(max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def get_read_num(self):
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']


class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    require = models.OneToOneField(Require, on_delete=models.DO_NOTHING)
