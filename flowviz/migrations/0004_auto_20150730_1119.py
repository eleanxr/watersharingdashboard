# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import flowviz.models


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0003_auto_20150728_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('description', models.CharField(max_length=1000)),
                ('start_date', models.DateField(default=flowviz.models.begin_default, null=True, blank=True)),
                ('end_date', models.DateField(default=flowviz.models.end_default, null=True, blank=True)),
                ('flow_data_file', models.FileField(null=True, upload_to=b'', blank=True)),
                ('date_column_name', models.CharField(max_length=80)),
                ('flow_column_name', models.CharField(max_length=80)),
            ],
        ),
        migrations.RemoveField(
            model_name='gradedflowtarget',
            name='begin_date',
        ),
        migrations.RemoveField(
            model_name='gradedflowtarget',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='gradedflowtarget',
            name='location',
        ),
        migrations.AddField(
            model_name='gradedflowtarget',
            name='description',
            field=models.CharField(default='Blank Description', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gradedflowtarget',
            name='watershed',
            field=models.ForeignKey(default=1, to='flowviz.Watershed'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scenario',
            name='flow_target',
            field=models.ForeignKey(to='flowviz.GradedFlowTarget'),
        ),
        migrations.AddField(
            model_name='scenario',
            name='gage_location',
            field=models.ForeignKey(blank=True, to='flowviz.GageLocation', null=True),
        ),
        migrations.AddField(
            model_name='scenario',
            name='watershed',
            field=models.ForeignKey(to='flowviz.Watershed'),
        ),
    ]
