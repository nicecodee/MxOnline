# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-24 23:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='', max_length=20, verbose_name='\u8bfe\u7a0b\u7c7b\u522b'),
        ),
        migrations.AlterField(
            model_name='course',
            name='learn_times',
            field=models.IntegerField(default=0, verbose_name='\u5b66\u4e60\u65f6\u957f(\u5206\u949f)'),
        ),
    ]
