# 使用 Django REST framework 实现后端 REST API
from rest_framework import serializers
# files 是 app 的名字
from files import models

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FilesModel
        fields = '__all__'

