from django import template
from .. models import Post, Category, Tag
from django.db.models.aggregates import Count


register = template.Library()


@register.inclusion_tag('web/inclusions/recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    post_list = Post.objects.all().order_by('-views')[:num]
    color = ['#f54646','#ff8648','#ffa82d','#8fb9f5','#8fb9f5']
    colornum = ['1','2','3','4','5']
    array = zip(post_list,color,colornum)
    return {
        'array':array
         # 定义文章列表,取前5
    }


@register.inclusion_tag('web/inclusions/archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),  # 定义归档函数
    }


@register.inclusion_tag('web/inclusions/categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }


@register.inclusion_tag('web/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }