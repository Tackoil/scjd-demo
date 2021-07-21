from django.db import models

# Create your models here.


# 企业分布饼图数据对象
class EpDistributionPieData(models.Model):
    # id: models.AutoField(primary_key=True)  # 自动计数主键
    name = models.CharField(max_length=32)
    value = models.IntegerField()


class NewsWordMapData(models.Model):
    word = models.CharField(max_length=32)
    value = models.IntegerField()


class PatentMap(models.Model):
    name = models.CharField(max_length=32)
    value = models.IntegerField()