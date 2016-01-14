# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0005_auto_20151207_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='GISLayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('project', models.ForeignKey(to='flowviz.Project')),
            ],
        ),
    ]
