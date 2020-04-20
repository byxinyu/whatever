from django.db import models
from django.utils import timezone
 
 
class Comment(models.Model):
    name = models.CharField('名字', max_length=50)
    email = models.EmailField('邮箱')
    url = models.URLField('网址', blank=True)
    text = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey('web.Post', verbose_name='文章', on_delete=models.CASCADE)
 
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
 
    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])

    def show_comments(context, post):
	    comment_list = post.comment_set.all().order_by('-created_time')
	    comment_count = comment_list.count()
	    return {
	        'comment_count': comment_count,
	        'comment_list': comment_list,
	    }


# Create your models here.
