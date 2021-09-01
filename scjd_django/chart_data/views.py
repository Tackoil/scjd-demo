from chart_data.models import Chart, FileHistory
from chart_data.filters import FileHistoryFilter
from chart_data.serializers import ChartSerializer, FileHistorySerializer, DisplaySerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, mixins
from rest_framework.decorators import action
from django.http import FileResponse
from pyexcel_xlsx import get_data


class ChartList(generics.ListCreateAPIView):
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer

    # 为满足动态fields的查询请求,重写get方法
    def get(self, request, format=None):
        charts = Chart.objects.all()
        try:
            fields = request.query_params.get('fields')
            fields_list = fields.split(',')
            # 验证field是否为Chart的字段
            for field in fields_list:
                if field not in ['name', 'type', 'display', 'removable', 'x_coordinate', 'y_coordinate', 'width', 'height', 'history']:
                    return Response(data={'message': "请求中包含错误的字段"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = ChartSerializer(charts, many=True, fields=fields_list)
        except Exception as e:
            serializer = ChartSerializer(charts, many=True)
        return Response(serializer.data)


class ChartDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer

    # 为满足动态fields的查询请求,重写get方法
    def get(self, request, format=None, *args, **kwargs):
        obj = self.get_object()
        try:
            fields = request.query_params.get('fields')
            fields_list = fields.split(',')
            # 验证field是否为Chart的字段
            for field in fields_list:
                if field not in ['name', 'type', 'display', 'removable', 'x_coordinate', 'y_coordinate', 'width', 'height', 'history']:
                    return Response(data={'message': "请求中包含错误的字段"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = ChartSerializer(obj, fields=fields_list)
        except Exception as e:
            serializer = ChartSerializer(obj)
        return Response(serializer.data)

    # 在删除前需要进行验证，只有当chart的removable属性为True时才能进行删除
    def destroy(self, request, format=None, *args, **kwargs):
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
    filter_class = FileHistoryFilter  # 过滤类

    # 此时访问 http://xx.xx.xx.xx:8000/chart-data/files/download/ 链接，根据chart的id和timestamp即可直接下载上传到服务器上的文件。
    # 会弹出一个下载框
    # 下载的文件名即为uploads文件夹中存储的文件名
    @action(methods=['get'], detail=False)
    def download(self, request, pk=None, *args, **kwargs):
        chart = request.query_params.get('chart')
        timestamp = request.query_params.get('timestamp')
        file_obj = FileHistory.objects.filter(
            chart=chart).filter(timestamp=int(timestamp)).first()
        response = FileResponse(open(file_obj.file_url.path, 'rb'))
        filename = str(file_obj.file_url).split("/")[1]
        # 弹出一个下载框
        # 注意不同浏览器对于下载文件文件名的编码解析格式不一样
        # 在后台把文件名先encode成bytes，再判断浏览器，根据不同的浏览器用相应的编码decode一下就好了
        # 常用浏览器解析格式。
        # IE浏览器，采用URLEncoder编码
        # Opera浏览器，采用filename*方式
        # Safari浏览器，采用ISO编码的中文输出
        # Chrome浏览器，采用Base64编码或ISO编码的中文输出
        # FireFox浏览器，采用Base64或filename*或ISO编码的中文输出
        response['Content-Disposition'] = 'attachment; filename=' + \
            filename.encode('utf-8').decode('ISO-8859-1')
        # response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response

    # 以json的格式返回用于绘图的数据
    # 根据文件的后缀进行不同的解析
    @action(methods=['get'], detail=False)
    def parse(self, request, pk=None, *args, **kwargs):
        chart = request.query_params.get('chart')
        timestamp = request.query_params.get('timestamp')
        file_obj = FileHistory.objects.filter(
            chart=chart).filter(timestamp=int(timestamp)).first()
        # 获取文件后缀
        file_suffix = str(file_obj.file_url).split(".")[1]
        # 如果是json文件直接返回，不需要用不同的方式进行数据解析
        # 总是假设上传的数据完全符合画图要求
        if file_suffix == 'json':
            response = FileResponse(open(file_obj.file_url.path, 'rb'))
            return response
        elif file_suffix == 'xlsx':
            # 解析Excel的xlsx格式文件
            # 首先要查询该文件对应图表的type
            # type=8：代表自定义折线图
            # type=9: 代表自定义柱状图
            # type=10: 代表自定义饼图
            data = get_data(file_obj.file_url)
            chart_obj = Chart.objects.get(id=chart)
            if(chart_obj.type == 8):
                json_data = {}
                data = data[list(data.keys())[0]]
                json_data["xAxis_data"] = data[0][1:]
                series = []
                for i in range(1, len(data)):
                    temp_dict = {'type': 'line'}
                    temp_dict['name'] = data[i][0]
                    temp_dict['data'] = data[i][1:]
                    series.append(temp_dict)
                json_data['series'] = series
            return Response(json_data)


class DisplayAPIView(APIView):
    # 实现大屏相关数据的群查
    def get(self, request, *args, **kwargs):
        display_query = Chart.objects.filter(display=True).all()
        serializer = DisplaySerializer(display_query, many=True)
        return Response(data=serializer.data)

    # 实现大屏相关数据的群改
    def put(self, request, *args, **kwargs):
        data = request.data

        # 更新一条数据
        # 接口为：http://127.0.0.1:8000/chart-data/display/?id=[id]
        if isinstance(data, dict):
            id = request.query_params.get('id')
            try:
                inst = Chart.objects.get(id=id)
            # 无效的id
            except Chart.DoesNotExist as e:
                return Response(data={'message': "试图更新的图表不存在"}, status=status.HTTP_404_NOT_FOUND)
            serializer = DisplaySerializer(
                instance=inst, data=data, many=False)
            if serializer.is_valid():
                serializer.save()
                # 更新成功以后返回更新后的大屏展示数据
                display_query = Chart.objects.filter(display=True).all()
                serializer = DisplaySerializer(display_query, many=True)
                datas = serializer.data
            else:
                datas = serializer.errors
            return Response(data=datas)

        # 更新一批数据
        elif isinstance(data, list):
            pk_objs = []
            for item in request.data:
                pk = item.pop("id")
                pk_objs.append(pk)
            objs = Chart.objects.filter(id__in=pk_objs)
            # 如果批量更新的数据中有无效的id
            if len(objs) != len(pk_objs):
                return Response(data={'message': "试图更新的图表不存在"}, status=status.HTTP_404_NOT_FOUND)
            serializer = DisplaySerializer(instance=objs, data=data, many=True)
            if serializer.is_valid():
                serializer.save()
                # 更新成功以后返回更新后的大屏展示数据
                display_query = Chart.objects.filter(display=True).all()
                serializer = DisplaySerializer(display_query, many=True)
                datas = serializer.data
                return Response(data=datas)
            else:
                datas = serializer.errors
                # 这里是强行让状态码为400，正确该怎么做呢？
                return Response(data=datas, status=status.HTTP_400_BAD_REQUEST)
            

    def patch(self, request, *args, **kwargs):
        data = request.data

        # 更新一条数据
        if isinstance(data, dict):
            id = request.query_params.get('id')
            try:
                inst = Chart.objects.get(id=id)
            # 无效的id
            except Chart.DoesNotExist as e:
                return Response(data={'message': "试图更新的图表不存在"}, status=status.HTTP_404_NOT_FOUND)
            serializer = DisplaySerializer(
                instance=inst, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                # 更新成功以后返回更新后的大屏展示数据
                display_query = Chart.objects.filter(display=True).all()
                serializer = DisplaySerializer(display_query, many=True)
                datas = serializer.data
            else:
                datas = serializer.errors
            return Response(data=datas)
        # 更新一批数据
        elif isinstance(data, list):
            pk_objs = []
            for item in request.data:
                pk = item.pop("id")
                pk_objs.append(pk)
            objs = Chart.objects.filter(id__in=pk_objs)
            # 如果批量更新的数据中有无效的id
            if len(objs) != len(pk_objs):
                return Response(data={'message': "试图更新的图表不存在"}, status=status.HTTP_404_NOT_FOUND)
            serializer = DisplaySerializer(
                instance=objs, data=data, many=True, partial=True)
            if serializer.is_valid():
                serializer.save()
                # 更新成功以后返回更新后的大屏展示数据
                display_query = Chart.objects.filter(display=True).all()
                serializer = DisplaySerializer(display_query, many=True)
                datas = serializer.data
            else:
                datas = serializer.errors
            return Response(data=datas)
