# Generated by Django 2.2.3 on 2020-06-13 10:13

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_post_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(upload_to='article/%Y%m%d', verbose_name='标题图'),
        ),
    ]