# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datafiles', '0001_initial'),
        ('econ', '0007_cropmixproductionpractice'),
    ]

    operations = [
        migrations.AddField(
            model_name='cropmix',
            name='crop_column_name',
            field=models.CharField(max_length=80, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='cropmix',
            name='excel_file',
            field=models.ForeignKey(blank=True, to='datafiles.DataFile', null=True),
        ),
        migrations.AddField(
            model_name='cropmix',
            name='sheet_name',
            field=models.CharField(max_length=80, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='cropmix',
            name='source_type',
            field=models.CharField(default=b'NASS', max_length=4, choices=[(b'NASS', b'USDA NASS'), (b'XLSX', b'Excel File')]),
        ),
        migrations.AddField(
            model_name='cropmix',
            name='unit_column_name',
            field=models.CharField(max_length=80, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='cropmix',
            name='year_column_name',
            field=models.CharField(max_length=80, null=True, blank=True),
        ),
    ]
