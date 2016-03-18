# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('econ', '0008_add_excel_columns'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumerPriceIndexData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('value', models.FloatField()),
            ],
        ),
    ]
