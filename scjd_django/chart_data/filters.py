#filters.py
from django_filters import rest_framework as filters

from chart_data.models import Chart, FileHistory


class FileHistoryFilter(filters.FilterSet):

    class Meta:
        model = FileHistory  # 模型名
        fields = ['chart','timestamp']   # 要过滤的字段


