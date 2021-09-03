from django.contrib import admin


from .models import Chart, FileHistory

# Register your models here.
@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    # 配置列表视图
    list_display = ['name','type', 'display', 'removable', 'x_coordinate', 'y_coordinate', 'width', 'height']
    # 添加列表过滤器
    list_filter = ('type', 'display', 'removable')


admin.site.register(FileHistory)
