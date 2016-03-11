# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-11 15:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20160311_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watching',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='core.Series'),
        ),
        migrations.AlterField(
            model_name='watching',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watches', to=settings.AUTH_USER_MODEL),
        ),
    ]
