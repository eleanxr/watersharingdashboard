# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0003_scenario_attribute_multiplier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scenario',
            name='attribute_name',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='attribute_units',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='attribute_units_abbr',
        ),
        migrations.AlterField(
            model_name='scenario',
            name='attribute_multiplier',
            field=models.FloatField(default=1.0, help_text=b'Input flow data must be reported in cubic feet per second (CFS). If your data is not already in CFS, then use this field to set the a multiplication value that will convert your data to CFS.'),
        ),
    ]
