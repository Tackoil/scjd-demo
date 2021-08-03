from chart_data.models import Chart, FileHistory
from chart_data.serializers import ChartSerializer, FileHistorySerializer, DisplaySerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, mixins
from rest_framework.decorators import action
from django.http import FileResponse


class ChartList(generics.ListCreateAPIView):
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer

    # 为满足动态fields的查询请求,重写get方法
    def get(self, request, format=None):
        charts = Chart.objects.all()
        try:
            fields = request.query_params.get('fields')
            fields_list = fields.split(',')
            serializer = ChartSerializer(charts, many=True, fields=fields_list)
        except Exception as e:
            serializer = ChartSerializer(charts, many=True)
        return Response(serializer.data)


class ChartDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer

    # 为满足动态fields的查询请求,重写get方法
    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            fields = request.query_params.get('fields')
            fields_list = fields.split(',')
            serializer = ChartSerializer(obj, fields=fields_list)
        except Exception as e:
            serializer = ChartSerializer(obj)
        return Response(serializer.data)

    # 在删除前需要进行验证，只有当chart的removable属性为True时才能进行删除
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.removable:
            return Response(data={'message': "图表不可删除"}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FileHistoryViewSet(ModelViewSet, mixins.DestroyModelMixin):
    # 查询所有信息
    queryset = FileHistory.objects.all()
    # 序列化
    serializer_class = FileHistorySerializer

    # 此时访问 http://xx.xx.xx.xx:8000/chart-data/files/download/ 链接，即可直接下载上传到服务器上的文件。
    @action(methods=['get', 'post'], detail=False)
    def download(self, request, pk=None, *args, **kwargs):
        chart = request.query_params.get('chart')
        timestamp = request.query_params.get('timestamp')
        file_obj = FileHistory.objects.filter(chart=chart).filter(timestamp=int(timestamp)).first()
        response = FileResponse(open(file_obj.json_url.path, 'rb'))
        return response


class DisplayAPIView(APIView):
    # 实现大屏相关数据的群查
    def get(self, request, *args, **kwargs):
        display_query = Chart.objects.filter(display=True).all()
        serializer = DisplaySerializer(display_query, many=True)
        return Response(data=serializer.data)

    # 实现大屏相关数据的群改
    def put(self, request, *args, **kwargs):
        data = request.data

        if kwargs.get("id") and isinstance(data, dict):
            inst = Chart.objects.filter(id=kwargs.get("id")).first()
            serializer = DisplaySerializer(
                instance=inst, data=data, many=False)
            if serializer.is_valid():
                serializer.save()
                datas = serializer.data
            else:
                datas = serializer.errors
            return Response(data=datas, status=200)
        elif isinstance(data, list):
            pk_objs = []
            for item in request.data:
                pk = item.pop("id")
                pk_objs.append(pk)
            objs = Chart.objects.filter(id__in=pk_objs)
            serializer = DisplaySerializer(instance=objs, data=data, many=True)
            if serializer.is_valid():
                serializer.save()
                datas = serializer.data
            else:
                datas = serializer.errors
            return Response(data=datas, status=200)

    def patch(self,request,*args,**kwargs):
        data=request.data
    
        if kwargs.get("id")and isinstance(data,dict):
            inst=Chart.objects.filter(id=kwargs.get("id")).first()
            serializer= DisplaySerializer(instance=inst, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                datas= serializer.data
            else:
                datas= serializer.errors
            return Response(data=datas, status=200)
        elif isinstance(data,list):
            many=True
            pk_objs=[]
            for item in request.data:
                pk=item.pop("id")
                pk_objs.append(pk)
            objs=Chart.objects.filter(id__in=pk_objs)
            serializer= DisplaySerializer(instance=objs, data=data, many=True,partial=True)
            if serializer.is_valid():
                serializer.save()
                datas= serializer.data
            else:
                datas= serializer.errors
            return Response(data=datas, status=200)
