from django.db import models

# Create your models here.
class FilesModel(models.Model):
    name = models.CharField(max_length=40, default='')
    type = models.CharField(max_length=20, default='')
    file = models.FileField(upload_to='uploads/')
    can_del = models.BooleanField(default=True) # 默认新创建的图表可以删除

    class Meta:
        db_table = 'files_storage'
        ordering = ['-id']


