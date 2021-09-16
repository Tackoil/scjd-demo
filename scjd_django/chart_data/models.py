from django.db import models

# 图表模型
class Chart(models.Model):
    # 图表的基本信息
    name = models.CharField(max_length=100, blank=False, default='未命名图表')
    type = models.IntegerField(blank=True, null=True) # 允许图表type为空
    display = models.BooleanField(default=False)
    removable = models.BooleanField(default=False)
    # 图表的位置与尺寸信息
    x_coordinate = models.IntegerField(default=0)
    y_coordinate = models.IntegerField(default=0)
    width = models.IntegerField(default=500)
    min_width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(default=500)
    min_height = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ('type',)
        db_table = 'chart_info'

    def __str__(self):
        """
        用于表示模型对象的字符串
        """
        return "{}_{}".format(self.type, self.name)

# 文件上传记录模型
class FileHistory(models.Model):
    chart = models.ForeignKey(
        Chart, related_name='history', on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.IntegerField(default=0)  # 时间戳由前端计算，后端只存储一个整数
    file_url = models.FileField(upload_to='uploads/')

    class Meta:
        db_table = 'file_history'
        ordering = ['-chart', '-timestamp']  # 以timestamp降序排列

    def __str__(self):
        """
        用于表示模型对象的字符串
        """
        return "{}_{}".format(self.chart, self.timestamp)
