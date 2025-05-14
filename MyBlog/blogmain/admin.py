from django.contrib import admin
from django.utils import timezone

from .models import Post, Category, Tag
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    
    # 列表页展示的字段
    list_display = ['title', 'category', 'created_time', 'modified_time', 'author']
    # 表单展现的字段
    fields = ['title', 'text', 'category', 'tags']

    # 当创建或修改一个对象时，会调用 save_model 方法来保存这个对象。
    # 只作用于管理界面创建或更新。
    def save_model(self, request, obj, form, change):
        
        """
        重写 save_model 方法
        request: 当前的 HTTP 请求对象
        obj: 当前正在保存的对象
        form: 表单对象
        change: 布尔值，True 表示更新现有对象，False 表示创建新对象
        """
        # 如果是更新现有对象，则 change 为 True
        if not change:
            
            obj.author = request.user

        # 需要在任何地方都生效可以使用 models.py 中的 save 方法。
        # obj.modified_time = timezone.now()
        super().save_model(request, obj, form, change)
        
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)