# Generated by Django 2.2.3 on 2020-06-13 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20200613_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='stick',
            field=models.NullBooleanField(verbose_name='置顶'),
        ),
    ]
