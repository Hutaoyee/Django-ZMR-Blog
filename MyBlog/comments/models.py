from django.db import models
from django.utils import timezone

# Create your models here.
class Comment(models.Model):
    
    name = models.CharField('名称', max_length=50)
    email = models.EmailField('邮箱')
    url = models.URLField('网址', blank=True)
    text = models.TextField('评论内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey('blogmain.Post', verbose_name='文章', on_delete=models.CASCADE)

    class Meta:
    
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
        
    def __str__(self):
        
        return '{} : {}'.format(self.name, self.text)
    
