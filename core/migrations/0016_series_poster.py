# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-09 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20160309_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='poster',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]