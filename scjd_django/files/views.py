from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from files import models, serializers
from django.http import FileResponse

# Create your views here.
class FileViewSet(ModelViewSet):
    queryset = models.FilesModel.objects.all()
    serializer_class = serializers.FilesSerializer

    # 此时访问 http://xx.xx.xx.xx:8000/storage/files/[id]/download/ 链接，即可直接下载上传到服务器上的文件。
    @action(methods=['get', 'post'], detail=True)
    def download(self, request, pk=None, *args, **kwargs):
        file_obj = self.get_object()
        response = FileResponse(open(file_obj.file.path, 'rb'))
        return response