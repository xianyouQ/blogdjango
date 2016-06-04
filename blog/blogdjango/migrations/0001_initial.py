# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 15:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(default=b'', max_length=200, verbose_name='\u535a\u6587\u7c7b\u578b')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u7c7b\u578b\u521b\u5efa\u65e5\u671f')),
            ],
            options={
                'ordering': ['create_time'],
                'db_table': 'blog_type',
                'verbose_name': '\u535a\u6587\u7c7b\u578b',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('blog_title', models.CharField(default=b'', max_length=200, verbose_name='blog\u540d\u79f0')),
            ],
            options={
                'ordering': ['create_time'],
                'db_table': 'blog',
                'verbose_name': '\u535a\u5ba2',
            },
        ),
        migrations.CreateModel(
            name='BlogPermisson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_priority', models.SmallIntegerField(choices=[(0, b'\xe6\x97\xa0\xe8\xaf\xbb\xe6\x9d\x83\xe9\x99\x90'), (1, b'\xe5\x8f\xaf\xe8\xaf\xbb'), (2, b'\xe5\x8f\xaf\xe8\xaf\x84\xe8\xae\xba')], default=0, verbose_name=b'\xe6\x9d\x83\xe9\x99\x90')),
                ('ask_time', models.DateTimeField(auto_now_add=True, verbose_name='\u8bf7\u6c42\u6743\u9650\u65f6\u95f4')),
                ('need_confirm', models.BooleanField(default=True, verbose_name='\u9700\u8981\u5ba1\u6838')),
            ],
            options={
                'ordering': ['ask_time'],
                'db_table': 'blog_permisson',
                'verbose_name': '\u535a\u5ba2\u6743\u9650',
            },
        ),
        migrations.CreateModel(
            name='BlogText',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u6587\u6863\u521b\u5efa\u65e5\u671f')),
                ('context', models.TextField(verbose_name='blogText\u5185\u5bb9')),
                ('blog_text_title', models.CharField(default=b'', max_length=400, verbose_name='blogText\u540d\u79f0')),
                ('is_publish', models.BooleanField(default=False, verbose_name='\u662f\u5426\u53ef\u4ee5\u5c55\u793a')),
                ('article_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogdjango.ArticleType')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogdjango.Blog')),
            ],
            options={
                'ordering': ['create_time'],
                'db_table': 'blog_text',
                'verbose_name': '\u535a\u5ba2\u6587\u6863',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.TextField()),
                ('comment_time', models.DateTimeField(auto_now_add=True, verbose_name='\u8bc4\u8bba\u65f6\u95f4')),
                ('blogtext', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogdjango.BlogText')),
            ],
            options={
                'ordering': ['comment_time'],
                'db_table': 'blog_comment',
                'verbose_name': '\u535a\u5ba2\u8bc4\u8bba',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(default=b'', max_length=200, verbose_name='\u804a\u5929\u6d88\u606f')),
                ('contact_time', models.DateTimeField(auto_now_add=True, verbose_name='\u804a\u5929\u65f6\u95f4')),
                ('is_read', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u8bfb')),
            ],
            options={
                'ordering': ['contact_time'],
                'db_table': 'blog_message',
                'verbose_name': '\u804a\u5929\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='ShortArticle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u6587\u6863\u521b\u5efa\u65e5\u671f')),
                ('context', models.TextField(verbose_name='\u5185\u5bb9')),
                ('short_text_title', models.CharField(default=b'', max_length=400, verbose_name='\u540d\u79f0')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogdjango.Blog')),
            ],
            options={
                'ordering': ['create_time'],
                'db_table': 'short_article',
                'verbose_name': '\u77ed\u535a\u6587',
            },
        ),
        migrations.CreateModel(
            name='ShortComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.TextField()),
                ('comment_time', models.DateTimeField(auto_now_add=True, verbose_name='\u8bc4\u8bba\u65f6\u95f4')),
            ],
            options={
                'ordering': ['comment_time'],
                'db_table': 'short_comment',
                'verbose_name': '\u77ed\u535a\u6587\u8bc4\u8bba',
            },
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(default=b'', max_length=200, verbose_name='\u6635\u79f0')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('is_active', models.BooleanField(default=False, verbose_name='\u662f\u5426\u901a\u8fc7\u5ba1\u6838')),
                ('need_confirm', models.BooleanField(default=True, verbose_name='\u9700\u8981\u5ba1\u6838')),
                ('signature', models.CharField(default=b'', max_length=400, verbose_name='\u4e2a\u6027\u7b7e\u540d')),
                ('askuser', models.ManyToManyField(related_name='Permission', through='blogdjango.BlogPermisson', to='blogdjango.UserDetail')),
                ('contact_user', models.ManyToManyField(related_name='Contact', through='blogdjango.Message', to='blogdjango.UserDetail')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['create_time'],
                'db_table': 'user_detail',
                'verbose_name': '\u7528\u6237\u8be6\u7ec6\u6570\u636e',
            },
        ),
        migrations.AddField(
            model_name='shortcomment',
            name='comment_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogdjango.UserDetail'),
        ),
        migrations.AddField(
            model_name='shortcomment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_comments', to='blogdjango.ShortComment'),
        ),
        migrations.AddField(
            model_name='shortcomment',
            name='shortarticle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogdjango.ShortArticle'),
        ),
        migrations.AddField(
            model_name='message',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sended_message', to='blogdjango.UserDetail'),
        ),
        migrations.AddField(
            model_name='message',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recived_message', to='blogdjango.UserDetail'),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blogdjango.UserDetail'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_comments', to='blogdjango.Comment'),
        ),
        migrations.AddField(
            model_name='blogpermisson',
            name='ask_from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_permissons', to='blogdjango.UserDetail'),
        ),
        migrations.AddField(
            model_name='blogpermisson',
            name='asked_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_asked_permisson', to='blogdjango.UserDetail'),
        ),
        migrations.AddField(
            model_name='blog',
            name='userDetail',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blogdjango.UserDetail'),
        ),
        migrations.AddField(
            model_name='articletype',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogdjango.Blog'),
        ),
    ]
