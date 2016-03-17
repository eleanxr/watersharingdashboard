# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('econ', '0006_auto_20160315_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='CropMixProductionPractice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('production_practice', models.CharField(max_length=80)),
                ('analysis', models.ForeignKey(to='econ.CropMix')),
            ],
        ),
    ]
