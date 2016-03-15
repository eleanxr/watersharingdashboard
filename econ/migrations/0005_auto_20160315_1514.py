# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('econ', '0004_cropmixgroup_niwr'),
    ]

    operations = [
        migrations.AddField(
            model_name='cropmixgroup',
            name='labor',
            field=models.DecimalField(default=0, help_text=b'Required labor in hours/acre', max_digits=10, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cropmixgroup',
            name='revenue',
            field=models.DecimalField(default=0, help_text=b'Revenue estimate in $/acre', max_digits=10, decimal_places=2),
            preserve_default=False,
        ),
    ]
