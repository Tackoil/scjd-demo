from django.contrib import admin

# Register your models here.
from .models import FilesModel

# admin.site.register(FilesModel)

@admin.register(FilesModel)
class FileAdmin(admin.ModelAdmin):
    # 配置列表视图
    list_display = ['name', 'type', 'file', 'can_del']
    # 添加列表过滤器
    list_filter = ('type', 'can_del')