from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from blogmain.models import Post

from .forms import CommentForm

# Create your views here.
# 限制这个视图只能通过 POST 请求触发。
@require_POST
def comment(request, post_pk):
    
    post = get_object_or_404(Post, pk=post_pk)
    # django 将用户提交的数据封装在 request.POST 中，这是一个类字典对象。
    form = CommentForm(request.POST)
    
    if form.is_valid():
        
        # 仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
        comment = form.save(commit = False)
        
        comment.post = post
        comment.save()
        
        # 发送的消息被缓存在 cookie。
        # extra_tags: 打上额外标签。
        messages.add_message(request, messages.SUCCESS, '评论成功!!!', extra_tags = 'success')
        
        # 重定向到 post 的详情页。
        return redirect(post)
    
    # 渲染一个预览页面，用于展示表单的错误。
    context = {
        
        'post' : post,
        'form' : form,
    }
    
    messages.add_message(request, messages.ERROR, '评论失败!!!', extra_tags = 'danger')
    return render(request, 'comments/preview.html', context = context)