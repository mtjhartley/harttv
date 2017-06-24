# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-24 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harttv_app', '0002_episode'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='episode_number',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='episode',
            name='season_number',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
