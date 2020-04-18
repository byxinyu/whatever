from django import template
from .. models import Post, Category, Tag


register = template.Library()


@register.inclusion_tag('web/inclusions/recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],  # 定义文章列表,取前5
    }


@register.inclusion_tag('web/inclusions/archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),  # 定义归档函数
    }


@register.inclusion_tag('web/inclusions/categories.html', takes_context=True)
def show_categories(context):
    return {
        'category_list': Category.objects.all(),
    }


@register.inclusion_tag('web/inclusions/tags.html', takes_context=True)  # 定义标签云函数
def show_tags(context):
    return {
        'tag_list': Tag.objects.all(),
    }