# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0002_auto_20150810_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario',
            name='attribute_multiplier',
            field=models.FloatField(default=1.0),
        ),
    ]
