# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-22 13:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogdjango', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortcomment',
            name='comment_to_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='short_comment_to', to='blogdjango.UserDetail'),
        ),
        migrations.AlterField(
            model_name='shortcomment',
            name='comment_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='short_comment_from', to='blogdjango.UserDetail'),
        ),
        migrations.AlterField(
            model_name='shortcomment',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
