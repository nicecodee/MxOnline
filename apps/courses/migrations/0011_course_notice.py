# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-26 09:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20170825_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='notice',
            field=models.CharField(default='', max_length=200, verbose_name='\u8bfe\u7a0b\u516c\u544a'),
        ),
    ]
