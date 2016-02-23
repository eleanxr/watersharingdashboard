# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import scenarios.models


class Migration(migrations.Migration):

    dependencies = [
        ('datafiles', '0001_initial'),
        ('watersheds', '0001_initial'),
        ('flowviz', '0016_rename_scenario_tables')
    ]

    # State operations only. flowviz 0016 renamed the tables to create them.
    state_operations = [
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
                ('target', models.ForeignKey(to='scenarios.CyclicTarget')),
            ],
        ),
        migrations.CreateModel(
            name='GageLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('watershed', models.ForeignKey(to='watersheds.Watershed')),
            ],
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField()),
                ('attribute_multiplier', models.FloatField(default=1.0, help_text=b'Input flow data must be reported in cubic feet per second (CFS). If your data is not already in CFS, then use this field to set the a multiplication value that will convert your data to CFS.')),
                ('source_type', models.CharField(default=b'GAGE', max_length=4, choices=[(b'GAGE', b'USGS Gage'), (b'XLSX', b'Excel File')])),
                ('parameter_code', models.CharField(default=b'00060', max_length=b'10', null=True, blank=True)),
                ('parameter_name', models.CharField(default=b'flow', max_length=b'20')),
                ('start_date', models.DateField(default=scenarios.models.begin_default, null=True, blank=True)),
                ('end_date', models.DateField(default=scenarios.models.end_default, null=True, blank=True)),
                ('sheet_name', models.CharField(max_length=80, null=True, blank=True)),
                ('date_column_name', models.CharField(max_length=80, null=True, blank=True)),
                ('attribute_column_name', models.CharField(max_length=80, null=True, blank=True)),
                ('target_column_name', models.CharField(max_length=80, null=True, blank=True)),
                ('excel_file', models.ForeignKey(blank=True, to='datafiles.DataFile', null=True)),
                ('gage_location', models.ForeignKey(blank=True, to='scenarios.GageLocation', null=True)),
                ('target', models.ForeignKey(blank=True, to='scenarios.CyclicTarget', null=True)),
            ],
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=state_operations
        )
    ]
