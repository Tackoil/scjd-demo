from rest_framework import serializers
from rest_framework.serializers import Field
from chart_data.models import Chart, FileHistory
from django.db.models import Max
# from datetime import datetime
# from pytz import timezone

# TIME_ZONE = 'Asia/Shanghai'

# class TimestampField(Field):
#     """
#     This serializer field transform a datetime str to a timestamp int
#     """

#     def to_representation(self, value):
#         return int(value.timestamp())

#     def to_internal_value(self, data):
#         timestamp = int(data)
#         no_tz = datetime.utcfromtimestamp(timestamp)
#         return no_tz.astimezone(timezone(TIME_ZONE))

# 自定义一个动态Field序列化器


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)  # 提取fields

        # 实例化父类
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # 删除fields参数中未指定的任何字段
            allowed = set(fields)
            existing = set(self.fields.keys())
            if allowed:
                for field_name in existing - allowed:
                    self.fields.pop(field_name)
            else:
                # fields参数为空，则取全部字段
                pass


# FileHistory序列化器继承自定义的动态Field序列化器
class FileHistorySerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = FileHistory
        fields = ['id', 'chart', 'timestamp', 'file_url']


# Chart序列化器继承自定义的动态Field序列化器
class ChartSerializer(DynamicFieldsModelSerializer):
    # 因为'history' 在用户模型中是一个反向关联关系。在使用 ModelSerializer 类时它默认不会被包含，所以我们需要为它添加一个显式字段。
    # history = serializers.PrimaryKeyRelatedField(many=True, queryset=FileHistory.objects.all())

    # 使用嵌套序列化器
    # history字段实际上对应的是一个FileHistory模型实例化后的对象
    history = FileHistorySerializer(many=True,
                                    read_only=True,
                                    fields=['timestamp', 'file_url'])

    class Meta:
        model = Chart
        fields = ['id', 'name', 'type', 'display', 'removable',
                  'x_coordinate', 'y_coordinate', 'width', 'height', 'history']
        read_only_fields = ['id', 'history']

    # 重写to_representation方法，改变序列化的输出
    def to_representation(self, value):
        # 调用父类获取当前序列化数据，value代表每个对象实例obj
        data = super().to_representation(value)
        # 对序列化数据做修改，只取最新的文件上传数据
        try:
            if data['history'] != []:
                data['history'] = data['history'][0]
        finally:
            return data

    # 重写to_internal_value方法
    def to_internal_value(self, data):
        # 提取所需要的数据，对其进行反序列化，data代表未验证的数据
        # 新生成的图表默认放在左下角
        if not data.get('y_coordinate'):
            if Chart.objects.all().exists():
                # 找到最下方的图表对象
                lowest_chart = Chart.objects.all().order_by('y_coordinate').last()
                # 新生成的图表的y坐标为目前最下方的图表对象的y坐标加上其高度
                data['y_coordinate'] = lowest_chart.y_coordinate + lowest_chart.height
        value = super().to_internal_value(data)
        return value



class DisplaySerializerList(serializers.ListSerializer):
    # create方法支持不必要重写
    # self.child就代表该ListSerializer类绑定的ModelSerializer类
    def update(self, instance_queryset, validated_data_list):
        queryset = []
        for index, validated_data in enumerate(validated_data_list):
            inst = self.child.update(instance_queryset[index], validated_data)
            queryset.append(inst)
        return queryset


# 大屏展示相关数据的序列化器
class DisplaySerializer(serializers.ModelSerializer):
    # 增加field验证
    id = serializers.IntegerField(read_only=True)
    x_coordinate = serializers.IntegerField(min_value=0, max_value=4000)
    y_coordinate = serializers.IntegerField(min_value=0, max_value=4000)
    width = serializers.IntegerField(min_value=0, max_value=4000)
    height = serializers.IntegerField(min_value=0, max_value=4000)
    display = serializers.BooleanField()

    class Meta:
        model = Chart
        fields = ['id', 'x_coordinate', 'y_coordinate',
                  'width', 'height', 'display']
        list_serializer_class = DisplaySerializerList
