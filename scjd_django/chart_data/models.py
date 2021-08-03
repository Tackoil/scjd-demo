from django.db import models


class Chart(models.Model):
    name = models.CharField(max_length=100, blank=False, default='未命名图表')
    type = models.IntegerField(default=1)
    display = models.BooleanField(default=False)
    removable = models.BooleanField(default=False)
    # 图表的位置与尺寸信息
    x_coordinate = models.IntegerField(default=0)
    y_coordinate = models.IntegerField(default=0)
    width = models.IntegerField(default=500)
    height = models.IntegerField(default=500)


    class Meta:
        ordering = ('type',)
        db_table = 'chart_info'

    def __str__(self):
        """
        用于表示模型对象的字符串
        """
        return "{}_{}".format(self.type, self.name)


class FileHistory(models.Model):
    chart = models.ForeignKey(Chart, related_name='history', on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.IntegerField(default=0) #时间戳由前端计算，后端只存储一个整数

    json_url = models.FileField(upload_to='uploads/')

    class Meta:
        db_table = 'file_history'
        ordering = ['-id']

    def __str__(self):
        """
        用于表示模型对象的字符串
        """
        return "{}_{}".format(self.chart, self.timestamp)

