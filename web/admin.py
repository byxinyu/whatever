from django.contrib import admin
from django.contrib import admin
from .models import Post, Category, Tag


class PosAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author', 'avatar']
    fields = ['title', 'body', 'excerpt', 'category', 'tags', 'avatar']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change);


admin.site.register(Post, PosAdmin)
admin.site.register(Category)
admin.site.register(Tag)
# Register your models here.
