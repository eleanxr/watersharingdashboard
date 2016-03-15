# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('econ', '0002_auto_20160311_1702'),
    ]

    operations = [
        migrations.CreateModel(
            name='CropMixGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=80)),
                ('analysis', models.ForeignKey(to='econ.CropMix')),
            ],
        ),
        migrations.CreateModel(
            name='CropMixGroupItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_name', models.CharField(max_length=80)),
                ('group', models.ForeignKey(to='econ.CropMixGroup')),
            ],
        ),
    ]
