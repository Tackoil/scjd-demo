from rest_framework import serializers
from rest_framework.serializers import Field
from chart_data.models import Chart, FileHistory
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
        fields = kwargs.pop('fields', None) # 提取fields
		
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
        fields = ['id', 'chart', 'timestamp', 'json_url']


# Chart序列化器继承自定义的动态Field序列化器
class ChartSerializer(DynamicFieldsModelSerializer):
    # 因为'history' 在用户模型中是一个反向关联关系。在使用 ModelSerializer 类时它默认不会被包含，所以我们需要为它添加一个显式字段。
    # history = serializers.PrimaryKeyRelatedField(many=True, queryset=FileHistory.objects.all())
    history = FileHistorySerializer(many=True, read_only=True, fields = ['timestamp', 'json_url'])

    class Meta:
        model = Chart
        fields = ['id', 'name','type', 'display', 'removable', 'x_coordinate', 'y_coordinate', 'width', 'height', 'history']


class DisplaySerializerList(serializers.ListSerializer):
    # create 支持不必要重写
    # self.child就代表该ListSerializer类绑定的ModelSerializer类
    def update(self, instance_queryset, validated_data_list):
        queryset=[]
        for index, validated_data in enumerate(validated_data_list):
            inst=self.child.update(instance_queryset[index], validated_data)
            queryset.append(inst)
        return queryset


# 大屏展示相关数据的序列化器
class DisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Chart
        fields = ['id', 'x_coordinate', 'y_coordinate', 'width', 'height'] 
        list_serializer_class= DisplaySerializerList

    