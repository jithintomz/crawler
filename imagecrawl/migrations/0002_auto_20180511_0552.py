# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-05-11 05:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagecrawl', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crawl',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='crawl',
            name='started_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='image',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
