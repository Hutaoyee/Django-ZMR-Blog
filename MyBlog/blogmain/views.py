from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.contrib.auth.models import User

from .models import Post, Category, Tag

from markdown import Markdown
from markdown.extensions.toc import TocExtension

import re
# Create your views here.
def index(request):
    
    post_list = Post.objects.all()
    
    return render(request, 'blogmain/index.html',
           
           context = {
               
               'title': 'Blog-main',
               'welcome': 'Welcome Back',
               'posts': post_list,
           }
    )

def detail(request, pk):
    
    # 当传入的 pk 对应的 Post 在数据库存在时，就返回对应的 post。
    post = get_object_or_404(Post, pk=pk)
    # post.context = markdown.markdown(post.context,
    #     extensions=[

    #         # extensions：它是对 Markdown 语法的拓展，
    #         # extra：基础拓展，
    #         # codehilite：语法高亮拓展，
    #         # toc：允许自动生成目录。
    #         'markdown.extensions.extra',
    #         'markdown.extensions.codehilite',
    #         'markdown.extensions.toc',
    #     ])
    
    # 实例化 markdown.Markdown 对象。
    md = Markdown(extensions = [
        
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        
        #  slugify 参数可以接受一个函数，这个函数将被用于处理标题的锚点值。
        #  django.utils.text 中的 slugify 方法，该方法可以更好地处理中文。
        TocExtension(slugify = slugify),
    ])
    
    # 将 post.text 转换为 HTML 格式。
    # 一旦调用该方法后，实例 md 就会多出一个 toc 属性，这个属性的值就是内容的目录。
    # 可在模板中使用该目录。
    post.text  = md.convert(post.text)
    
    # 目录为空则设置为空字符
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc  = m.group(1) if m else ''

    return render(request, 'blogmain/detail.html', context = {'post' : post})

def archive(request, year, month):
    
    # 作为方法的参数列表，所以 django 要求把点替换成了两个下划线。
    post_list = Post.objects.filter(created_time__year = year,
                                    created_time__month = month
                                    )
    
    return render(request, 'blogmain/index.html', context = {'posts' : post_list})

def category(request, pk):
    
    cate = get_object_or_404(Category, pk = pk)
    post_list = Post.objects.filter(category = cate)
    
    return render(request, 'blogmain/index.html', context = {'posts' : post_list})

def tag(request, pk):
    
    t = get_object_or_404(Tag, pk = pk)
    post_list = Post.objects.filter(tags = t)
    
    return render(request, 'blogmain/index.html', context = {'posts' : post_list})

def author(request, pk):
    
    aut = get_object_or_404(User, pk = pk)
    post_list = Post.objects.filter(author = aut)
    
    return render(request, 'blogmain/index.html', context = {'posts': post_list})