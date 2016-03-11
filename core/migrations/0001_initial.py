# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-11 16:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.PositiveIntegerField()),
                ('episode', models.PositiveIntegerField()),
                ('air_date', models.DateField(null=True)),
            ],
            options={
                'ordering': ['season', 'episode'],
            },
        ),
        migrations.CreateModel(
            name='LastUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tvdbid', models.PositiveIntegerField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.CharField(max_length=255)),
                ('banner', models.CharField(max_length=255)),
                ('poster', models.CharField(max_length=255)),
                ('first_aired', models.DateField(null=True)),
                ('imdb', models.CharField(max_length=1023)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Watching',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_seen', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('active', ''), ('default', ''), ('archived', '')], default='default', max_length=255)),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='core.Series')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watches', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='episode',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='core.Series'),
        ),
        migrations.AlterUniqueTogether(
            name='episode',
            unique_together=set([('series', 'season', 'episode')]),
        ),
    ]
