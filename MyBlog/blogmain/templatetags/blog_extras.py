from django import template

from ..models import Post, Category, Tag

# 模板标签库： 注册自定义模板标签和过滤器
register = template.Library()

# 最新文章
# 传入到第一个参数中
@register.inclusion_tag('blogmain/inclusions/_recent_posts.html', takes_context=True)
# num：默认显示的文章数量
def show_recent_posts(context, num = 5):
    
    return {
        
        'recent_posts_list' : Post.objects.all().order_by('-created_time')[:num],
    }

# 归档
@register.inclusion_tag('blogmain/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    
    return {
        
        #  Post.objects.dates：返回一个列表，列表中的元素为每一篇文章（Post）的创建时间（已去重），
        # 且是 Python 的 date 对象，精确到月份，降序排列。
        'date_list' : Post.objects.dates('created_time', 'month', order = 'DESC'),
    }
    
# 分类
@register.inclusion_tag('blogmain/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    
    return {
        
        'category_list' : Category.objects.all(),
    }
    
# 标签
@register.inclusion_tag('blogmain/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    
    return {
        
        'tag_list' : Tag.objects.all(),
    }