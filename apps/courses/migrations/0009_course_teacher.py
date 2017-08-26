# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-25 16:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_teacher_image'),
        ('courses', '0008_video_learn_times'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.Teacher', verbose_name='\u8bb2\u5e08'),
        ),
    ]
