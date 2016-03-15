# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('econ', '0003_cropmixgroup_cropmixgroupitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cropmixgroup',
            name='niwr',
            field=models.FloatField(default=0.0, help_text=b'Net irrigation water requirement'),
        ),
    ]
