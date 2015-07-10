# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GageLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='GradedFlowTarget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('location', models.ForeignKey(to='flowviz.GageLocation')),
            ],
        ),
        migrations.CreateModel(
            name='GradedFlowTargetElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_month', models.IntegerField()),
                ('from_day', models.IntegerField()),
                ('to_month', models.IntegerField()),
                ('to_day', models.IntegerField()),
                ('target_value', models.DecimalField(max_digits=8, decimal_places=2)),
                ('flow_target', models.ForeignKey(to='flowviz.GradedFlowTarget')),
            ],
        ),
        migrations.CreateModel(
            name='Watershed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='gagelocation',
            name='watershed',
            field=models.ForeignKey(to='flowviz.Watershed'),
        ),
    ]
