# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import flowviz.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CyclicTarget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CyclicTargetElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_month', models.IntegerField()),
                ('from_day', models.IntegerField()),
                ('to_month', models.IntegerField()),
                ('to_day', models.IntegerField()),
                ('target_value', models.DecimalField(max_digits=8, decimal_places=2)),
                ('target', models.ForeignKey(to='flowviz.CyclicTarget')),
            ],
        ),
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_file', models.FileField(upload_to=b'data-files')),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField()),
                ('uploaded_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GageLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField()),
                ('source_type', models.CharField(default=b'GAGE', max_length=4, choices=[(b'GAGE', b'USGS Gage'), (b'XLSX', b'Excel File')])),
                ('parameter_code', models.CharField(default=b'00060', max_length=b'10', null=True, blank=True)),
                ('parameter_name', models.CharField(default=b'flow', max_length=b'20')),
                ('start_date', models.DateField(default=flowviz.models.begin_default, null=True, blank=True)),
                ('end_date', models.DateField(default=flowviz.models.end_default, null=True, blank=True)),
                ('sheet_name', models.CharField(max_length=80, null=True, blank=True)),
                ('date_column_name', models.CharField(max_length=80, null=True, blank=True)),
                ('attribute_column_name', models.CharField(max_length=80, null=True, blank=True)),
                ('target_column_name', models.CharField(max_length=80, null=True, blank=True)),
                ('excel_file', models.ForeignKey(blank=True, to='flowviz.DataFile', null=True)),
                ('gage_location', models.ForeignKey(blank=True, to='flowviz.GageLocation', null=True)),
                ('project', models.ForeignKey(to='flowviz.Project')),
                ('target', models.ForeignKey(blank=True, to='flowviz.CyclicTarget', null=True)),
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
            model_name='project',
            name='watershed',
            field=models.ForeignKey(to='flowviz.Watershed'),
        ),
        migrations.AddField(
            model_name='gagelocation',
            name='watershed',
            field=models.ForeignKey(to='flowviz.Watershed'),
        ),
    ]
