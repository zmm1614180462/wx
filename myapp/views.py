from django.core.cache import cache
from django.utils.timezone import now
import logging #使用日志

import datetime
# Create your views here.
logger = logging.getLogger('myapp.views')
# -*- coding: utf-8 -*-
import logging
from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db import connection
from django.db.models import Count
from .models import *
from .forms import *
import json

# logger = logging.getLogger('blog.views')

# Create your views here.
def global_setting(request):
    # 站点基本信息
    SITE_URL = settings.SITE_URL
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    # 分类信息获取（导航数据）
    category_list = Category.objects.exclude(name='about').exclude(name='留言板')
    # 文章归档数据
    # archive_list = Article.objects.distinct_date()
    # 广告数据
    # 标签云数据
    # 友情链接数据
    # 文章排行榜数据（按浏览量和站长推荐的功能同学们自己完成）
    # 评论排行

    return locals()

def getPage(request, article_list):
    paginator = Paginator(article_list, 2)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)

    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    #文章归档
    #1.先找到要获取的文章有的年份月份 2015/06文章归档
    return article_list


def index(request):
    try:
        # 最新文章数据 [0:6:6]可以写成配置
        article_list = Article.objects.filter(is_recommend=1).order_by('-date_publish')[0:6]
    except Exception as e:
        logger.error(e)
    return render(request, 'wx/index.html', locals())

def category(request):
    try:
        cid = request.GET.get('cid',None)
        try:
            category = Category.objects.get(pk=cid)
        except Category.DoesNotExist:

            return render(request,'failure.html',{'reason': '分类不存在'})
        article_list = Article.objects.filter(category=category)
        article_list = getPage(request,article_list)
    except Exception as e:
        logger.error(e)
    return render(request,'category.html',locals())

def article(request):

    try:
        try:
            id = request.GET.get('id',None)
            #get如果找不到会抛出异常 DoesNotExist

            article = Article.objects.get(pk=id)
            #下一篇文章链接 上一篇文章链接
            article_last = Article.objects.filter(pk=int(id)-1)
            article_next = Article.objects.filter(pk=int(id)+1)
        except Article.DoesNotExist:
            return render(request,'failure.html',{'reason': '没有找到对应的文章'})
        #提交评论表单
        comment_form = CommentForm(
            {'author': request.user.username,
                                'email': request.user.email,
                                'url': request.user.url,
                                'article': id}if request.user.is_authenticated() else{'article': id})
        #获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item,'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)
    except Exception as e:
        logger.error(e)
    return render(request,'wx/article_content.html',locals())


#归档
def archive(request):
    try:
        year = request.GET.get('year',None)
        month = request.GET.get('month', None)
        article_list = Article.objects.filter(date_publish__icontains =year+'-'+month)
        article_list = getPage(request,article_list)

    except Exception as e:
        logger.error(e)

    return render(request, 'archive.html',locals())

#获取最近推荐文章
def recommend(request):
    article = Article.objects.filter(is_recommend=1).order_by('date_publish')
    return render(request,'wx/index.html',{article:article})
#登出

#about
def about(request):
    article = Article.objects.get(title='about')
    #{about:article}
    return render(request,'wx/about.html',locals())

def do_logout(request):
    pass

def comment_post(request):
    pass

def title(request):
    id = request.GET.get('id')
    category = request.GET.get('category')
    article_list = Article.objects.filter(category_id=id).order_by('date_publish')
    return render(request,'wx/article.html',locals())