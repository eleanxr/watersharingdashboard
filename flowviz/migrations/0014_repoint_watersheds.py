# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    # This migration depends on the database change that renames the watershed
    # table and on the state change that creates the model in the watersheds
    # application.
    dependencies = [
        ('flowviz', '0013_rename_watershed_table'),
        ('watersheds', '0001_initial')
    ]

    operations = [
        migrations.AlterField(
            model_name='gagelocation',
            name='watershed',
            field=models.ForeignKey(to='watersheds.Watershed'),
        ),
        migrations.AlterField(
            model_name='project',
            name='watershed',
            field=models.ForeignKey(to='watersheds.Watershed'),
        ),
    ]
