# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('econ', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('system', models.CharField(max_length=10)),
                ('key', models.CharField(max_length=80)),
                ('use_key', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='NASSApiKey',
        ),
        migrations.AddField(
            model_name='cropmix',
            name='cpi_adjustment_year',
            field=models.IntegerField(default=2014),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cropmix',
            name='source',
            field=models.CharField(default=b'CENSUS', max_length=20),
        ),
    ]
