# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-23 15:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20170623_0144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='comment_text',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='message',
            new_name='message_text',
        ),
    ]
