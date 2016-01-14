# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0004_auto_20150925_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='HUCRegion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hucid', models.CharField(max_length=12)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='huc_scale',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='hucregion',
            name='project',
            field=models.ForeignKey(to='flowviz.Project'),
        ),
    ]
