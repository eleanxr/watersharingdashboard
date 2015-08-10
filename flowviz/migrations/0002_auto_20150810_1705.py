# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario',
            name='attribute_name',
            field=models.CharField(default=b'Flow', max_length=80),
        ),
        migrations.AddField(
            model_name='scenario',
            name='attribute_units',
            field=models.CharField(default=b'Cubic Feet per Second', max_length=80),
        ),
        migrations.AddField(
            model_name='scenario',
            name='attribute_units_abbr',
            field=models.CharField(default=b'cfs', max_length=10),
        ),
    ]
