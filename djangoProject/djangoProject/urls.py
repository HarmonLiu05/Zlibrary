from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    path('accounts/', include('django.contrib.auth.urls')), # 自动处理登录退出
]