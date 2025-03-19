"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
import logging

# 设置日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 创建控制台处理器
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# 添加格式化器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 将处理器添加到记录器
logger.addHandler(handler)

# 记录调试信息
logger.debug("正在加载 DjangoProject/urls.py")

# 只保留一个 urlpatterns 定义
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Web 视图 URL
    path('accounts/', include('accounts.urls')),
    path('grades/', include('grades.urls')),  # 添加grades的web视图URL
    path('common/', include('common.urls')),  # 添加common的URL配置
    path('announcements/', include('announcements.urls')),  # 添加announcements的web视图URL
    
    # API URL
    path('api/accounts/', include('accounts.api_urls')),
    path('api/grades/', include('grades.urls')),
    path('api/announcements/', include('announcements.urls')),
    
    # 根 URL 重定向到 /accounts/login/
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False), name='root_redirect'),
]

# 记录 urlpatterns 已加载
logger.debug(f"urlpatterns 已加载，包含 {len(urlpatterns)} 个路径")

# 在开发环境中提供静态文件和媒体文件
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

