from django.shortcuts import render
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

class IndexView(PaginationMixin,ListView):
    model = Post
    template_name = 'web/index.html'
    context_object_name = 'post_list'
    # 指定paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 10

# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)

#     #阅读量 +1
#     post.increase_views()

#     md = markdown.Markdown(extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                       # 'markdown.extensions.fenced_code',
#                                       TocExtension(slugify=slugify),
#     ])
#     post.body = md.convert(post.body)
#     m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#     post.toc = m.group(1) if m is not None else ''
#     return render(request, 'web/detail.html', context={'post': post})


class PostDetailView(DetailView):
    #这些属性的含义和ListView 一样的
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

    def get_object(self,queryset=None):
        # 覆写 get_object 方法的目的是因为需要对post的body的值进行渲染
        post =super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 记得在顶部引入TocExtension 和 Slugify
            TocExtension(slugify=slugify),
            ])
        post.body = md.convert(post.body)

        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''

        return post


# def archive(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month
#                                     ).order_by('-created_time')
#     return render(request, 'web/index.html', context={'post_list': post_list})
class ArchiveView(ListView):
    model = Post
    template_name = 'web/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super().get_queryset().filter(created_time__year=year,created_time__month=month)


# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request, 'web/index.html', context={'post_list': post_list})

class CategoryView(IndexView):

    def get_queryset(self):
        cate = get_object_or_404(category, pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate)

# def tag(request, pk):
#     t = get_object_or_404(Tag, pk=pk)
#     post_list = Post.objects.filter(tags=t)
#     return render(request, 'web/index.html', context={'post_list': post_list})

class TagView(ListView):
    model = Tag
    template_name = 'web/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tag=t)

# Create your views here.

# def search(request):
#     q = request.GET.get('q')

#     if not q:
#         error_msg = "请输入搜索关键词"
#         messages.add_message(request,messages.ERROR, error_msg, extra_tags='danger')
#         return redirec('blog:index')

#     post_list = Post.objects.filter(Q(title_icontains=q) | Q(body_icontains=q))
#     return render(request, 'web/index.html', {'post_list':post_list})
def search(request):
    q = request.GET.get('q')
 
    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('web:index')
 
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'web/index.html', {'post_list': post_list})