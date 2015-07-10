# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gagelocation',
            name='description',
            field=models.CharField(default='No Description', max_length=200),
            preserve_default=False,
        ),
    ]
