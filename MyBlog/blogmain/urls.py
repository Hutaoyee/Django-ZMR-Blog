from django.urls import path

from . import views

# 视图函数命名空间：防止域名冲突，使用 `blogmain.<name>` 等明确引用。
app_name = 'blogmain'
urlpatterns = [
    
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.detail, name='detail'),
    # 归档文章列表
    path('archives/<int:year>/<int:month>/', views.archive, name='archives'),
    # 类型文章列表
    path('categories/<int:pk>/', views.category, name='category'),
    # 标签文章列表
    path('tags/<int:pk>/', views.tag, name='tag'),
    # 作者文章列表
    path('authors/<int:pk>/', views.author, name='author'),
]