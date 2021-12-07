from django.contrib import admin
from .models import Require, RequireType, ReadNum


# Register your models here.

@admin.register(RequireType)
class RequireTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(Require)
class RequireAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'require_type','author','get_read_num', 'created_time', 'last_updated_time')


@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'require')
