# 表单代码
from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    
    class Meta:
        
        model = Comment
        # 表单需要显示的字段
        # django 会自动将 fields 中声明的模型字段设置为表单的属性。
        fields = ['name', 'email', 'url', 'text']