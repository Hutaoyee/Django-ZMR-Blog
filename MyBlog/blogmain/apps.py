from django.apps import AppConfig


class BlogmainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blogmain'

    # 在 admin 显示的名称
    verbose_name = '博客模型'