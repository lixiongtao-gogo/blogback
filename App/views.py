import os
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.


from django.urls import reverse

from App.fileupload import FileUpload
from App.models import Category, Article, User
from App.verification import vc

#首页
def index(request):
    if not request.session.get('username'):
        return redirect(reverse('App:login'))
    return render(request,'index.html')

#左边窗口
def public_left(request):
    if not request.session.get('username'):
        return render(request,'loginb.html')
    return render(request,'public_left.html')

#右边上面
def public_header(request):
    if request.session.get('username'):
        username = request.session.get('username')
    else:
        return render(request,'loginb.html')

    return render(request,'public_header.html',locals())

#右边下面
def wenzhang_xinwen(request,cid = -1,page=1):
    if request.session.get('username'):
        #拿到分类数据库里面的内容
        categories = Category.objects.all()
        if cid < 0:
            first_cate = categories.first()
            cid = first_cate.c_id
        articles = Article.objects.filter(c_id=cid)
        content = request.POST.get('search')
        # print(content)
        if content:
            res = articles.filter(a_title__contains=content).first()
        num = articles.count()
        paginator = Paginator(articles,2)
        pager = paginator.page(page)
    else:
        return redirect(reverse('App:login'))
    return render(request,'wenzhang_xinwen.html',locals())

#文章发布
def wenzhang_xinwen_fabu(request):
    if request.session.get('username'):
        categorise = Category.objects.all()
        fobj = request.FILES.get('photo')
        path = settings.MDEIA_ROOT
        fp = FileUpload(fobj)
        path_photo = os.path.join('/static/img/' + str(fobj))
        if request.method == 'POST':
            #获取表单提交的信息
            cate = request.POST.get('cate')
            c_id = Category.objects.filter(c_name=cate).first().c_id
            a_title = request.POST.get('title')
            a_content = request.POST.get('content')
            a_time = datetime.now()

            if fp.Upload(path):
                print(path_photo)
                if a_title and a_content:
                    article = Article(a_title=a_title, a_content=a_content, a_create_time=a_time, c_id=c_id,
                                      a_picture=path_photo)
                    article.save()
    else:
        return redirect(reverse('App:login'))

    return render(request,'wenzhang_xinwen_fabu.html',locals())

#文件上传
# def file_upload(request):
#     if request.method == 'POST':
#         fobj = request.FILES.get('photo')
#         path = settings.MDEIA_ROOT
#         fp = FileUpload(fobj)
#         # path_photo = file_upload(request)
#
#         if fp.Upload(path):
#             return redirect('App:left_article')

#登录页面
def loginb(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        verify = request.POST.get('verifycode')
        res = User.objects.filter(u_username=username,u_psd=password)
        # print(username,password)
        if res and verify == request.session.get('code'):
            request.session['username'] = username

            return redirect(reverse('App:index'))
        else:
            messages.add_message(request, messages.ERROR, '用户名或者密码错误',extra_tags='alert alert-danger')
    return render(request,'loginb.html',locals())


#登出
def outlogin(request):
    request.session.flush()
    return redirect(reverse('App:login'))

#验证码
def verify(request):
    #获取图片
    res = vc.generate()
    #将验证码进行session设置
    request.session['code'] = vc.code
    response = HttpResponse(res,content_type='image/png')
    return response

#文章删除
def article_delete(request,aid,cid=-1,page=1):
    article_del = Article.objects.filter(a_id=aid)
    if article_del:
        article_del.delete()

    return redirect(reverse('App:low',kwargs={'cid':cid,'page':page}))



#分类页面
def fenlei_xinwen_fabu(request):
    if request.session.get('username'):
        categories = Category.objects.all()
        if request.method == 'POST':
            category = request.POST.get('category')
            for cate in categories:
                if category == cate.c_name:
                    messages.add_message(request, messages.ERROR, '分类重复', extra_tags='alert alert-danger')
                    return render(request, 'fenlei_xinwen_fabu.html', locals())
            else:
                cate = Category(c_name=category)
                cate.save()
                return redirect(reverse('App:left_cate'))
    else:
        return redirect(reverse('App:login'))
    return render(request, 'fenlei_xinwen_fabu.html', locals())


