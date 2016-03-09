# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CropMix',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField(null=True)),
                ('state', models.CharField(max_length=2)),
                ('county', models.CharField(max_length=40)),
                ('source', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CropMixCommodity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('commodity', models.CharField(max_length=80)),
                ('analysis', models.ForeignKey(to='econ.CropMix')),
            ],
        ),
        migrations.CreateModel(
            name='CropMixYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('analysis', models.ForeignKey(to='econ.CropMix')),
            ],
        ),
        migrations.CreateModel(
            name='NASSApiKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('key', models.CharField(max_length=80)),
                ('use_key', models.BooleanField(default=False)),
            ],
        ),
    ]
