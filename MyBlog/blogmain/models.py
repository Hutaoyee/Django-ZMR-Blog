from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    
    name = models.CharField(max_length=100)
    
    # 配置特性的类
    class Meta:
        
        # 在 admin 中的显示名称
        verbose_name = '类型'
        # 复数形式
        verbose_name_plural = verbose_name
    
    def __str__(self):
        
        return self.name

class Tag(models.Model):
    
    name = models.CharField(max_length=100)

    class Meta:
        
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        
        return self.name
    
class Post(models.Model):
    
    title = models.CharField('标题', max_length=100)
    
    text = models.TextField('正文')
    
    created_time = models.DateTimeField('创建时间', default = timezone.now)
    modified_time = models.DateTimeField('修改时间', )
    
    # 关系类型的第一位参数必须为关联模型，故使用 verbose_name 定义 admin 显示的名称。
    author = models.ForeignKey(User, verbose_name = '作者', on_delete=models.SET_DEFAULT, default = 1)
    
    category = models.ForeignKey(Category, verbose_name = '类型', on_delete=models.SET_DEFAULT, default = 1)
    tags = models.ManyToManyField(Tag, verbose_name = '标签', blank = True)
    
    class Meta:
        
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        # 指定文章排序方式: 按照文章发布时间排序，负号表示逆序排列
        ordering = ['-created_time']
    
    def __str__(self):
        
        return self.title
    
    # 每一个 Model 都有一个 save 方法，这个方法包含了将 model 数据保存到数据库中的逻辑。
    # 也可使用 admin.py 中的 savae_model 方法来实现。
    def save(self, *args, **kwargs):
        
        self.modified_time = timezone.now()
        super().save(*args, **kwargs)
    
    # 固定名称。
    def get_absolute_url(self):
        
        # reverse() 方法用于生成URL。
        # kwargs 是一个字典，包含了 URL 中的参数。
        return reverse('blogmain:detail', kwargs={'pk': self.pk})