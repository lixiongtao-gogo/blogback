"""blogback URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from App import views

app_name = 'App'

urlpatterns = [
    #首页
    path('', views.index,name='index'),
    #左边窗口
    path('left/',views.public_left,name='left'),
    #右边上边
    path('header/',views.public_header,name='header'),
    #右边下边
    path('low/',views.wenzhang_xinwen,name='low'),
    path('low/<int:cid>/',views.wenzhang_xinwen,name='low'),
    #分页
    path('low/<int:cid>/<int:page>/',views.wenzhang_xinwen,name='low'),

    #文章发布
    path('left_ariticle/',views.wenzhang_xinwen_fabu,name='left_article'),

    #登录页面
    path('login/',views.loginb,name='login'),

    #退出登录
    path('outlogin/',views.outlogin,name='outlogin'),

    #验证码
    path('verify/',views.verify,name='verify'),

    #文章删除
    path('delete/<int:cid>/<int:page>/<int:aid>/',views.article_delete,name='delete'),

    #添加分类
    path('left_cate',views.fenlei_xinwen_fabu,name='left_cate'),

    #上传文件
    # path('upload/',views.file_upload,name='upload'),


]
