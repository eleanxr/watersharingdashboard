# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import flowviz.models


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0004_auto_20150730_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_file', models.FileField(upload_to=b'data-files')),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ExcelDataSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sheet_name', models.CharField(max_length=80)),
                ('date_column_name', models.CharField(max_length=80)),
                ('flow_column_name', models.CharField(max_length=80)),
                ('target_column_name', models.CharField(max_length=80)),
                ('excel_file', models.ForeignKey(to='flowviz.DataFile')),
            ],
        ),
        migrations.CreateModel(
            name='GageDataSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(default=flowviz.models.begin_default)),
                ('end_date', models.DateField(default=flowviz.models.end_default)),
                ('gage_location', models.ForeignKey(to='flowviz.GageLocation')),
                ('graded_flow_target', models.ForeignKey(to='flowviz.GradedFlowTarget')),
            ],
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='date_column_name',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='flow_column_name',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='flow_data_file',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='flow_target',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='gage_location',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='start_date',
        ),
        migrations.AddField(
            model_name='scenario',
            name='source_type',
            field=models.CharField(default=b'GAGE', max_length=4, choices=[(b'GAGE', b'USGS Gage'), (b'XLSX', b'Excel File')]),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='description',
            field=models.TextField(),
        ),
        migrations.AddField(
            model_name='scenario',
            name='excel_data',
            field=models.ForeignKey(blank=True, to='flowviz.ExcelDataSource', null=True),
        ),
        migrations.AddField(
            model_name='scenario',
            name='gage_data',
            field=models.ForeignKey(blank=True, to='flowviz.GageDataSource', null=True),
        ),
    ]
