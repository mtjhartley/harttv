# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-28 18:36
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_registration', '0002_user_admin'),
        ('harttv_app', '0008_episodecomment_episoderating'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShowRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='show_ratings', to='harttv_app.Show')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_show_ratings', to='login_registration.User')),
            ],
        ),
    ]
