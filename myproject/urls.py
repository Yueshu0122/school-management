from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# 直接在主URLs文件中定义重定向函数
def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    # 直接在项目的URLs中处理根路径
    path('', redirect_to_login, name='home'),
    # 包含accounts应用的其他URLs
    path('accounts/', include('accounts.urls')),
    # 其他应用的URL配置...
] 