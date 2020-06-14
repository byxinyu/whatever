from django.http import HttpResponse
from .models import Post, Category, Tag
from django.shortcuts import render, get_object_or_404
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView
from django.views.generic import DetailView
from pure_pagination.mixins import PaginationMixin
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView


class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'web/index.html'
    context_object_name = 'post_list'
    # 指定paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 10




class PostDetailView(DetailView):
    model = Post
    template_name ='web/detail.html'
    context_object_name = 'post'

    def get(self, request,*args,**kwargs):
        # 覆写 get方法的目的是因为每当文章被访问一次，就将文章阅读量加1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的get方法，是因为只有当get 方法被调用后
        # 才有self。object属性，其值为Post模型实例，即被访问的文章POST
        response = super(PostDetailView,self).get(request,*args,**kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        #视图必须 返回一个HttpResponse对象
        return response
    

class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        return (
            super()
            .get_queryset()
            .filter(created_time__year=year, created_time__month=month)
        )


# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request, 'web/index.html', context={'post_list': post_list})

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get("pk"))
        return super().get_queryset().filter(tags=t)


def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return render('web:index')

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'web/index.html', {'post_list': post_list})


def about(request):
    q = request.GET.get('q')
 
    
 
    post_list = 'a';
    return render(request,'web/about.html',{'post_list': post_list});

def contact(request):
    q = request.GET.get('q')
 
    
 
    post_list = 'a';
    return render(request,'web/contact.html',{'post_list': post_list});


class fullwidthView(PaginationMixin,ListView):
    model = Post
    template_name = 'web/fullwidth.html'
    context_object_name = 'post_list'
    # 指定paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 10