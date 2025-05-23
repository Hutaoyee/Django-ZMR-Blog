"""
WSGI config for Blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# 使用 gunicorn 运行项目时，使用 production.py 的设置。
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog.settings.production')

application = get_wsgi_application()
