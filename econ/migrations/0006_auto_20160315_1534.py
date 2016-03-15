# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('econ', '0005_auto_20160315_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cropmixgroup',
            name='labor',
            field=models.FloatField(help_text=b'Required labor in hours/acre'),
        ),
        migrations.AlterField(
            model_name='cropmixgroup',
            name='niwr',
            field=models.FloatField(default=0.0, help_text=b'Net irrigation water requirement in ft/acre'),
        ),
        migrations.AlterField(
            model_name='cropmixgroup',
            name='revenue',
            field=models.FloatField(help_text=b'Revenue estimate in $/acre'),
        ),
    ]
