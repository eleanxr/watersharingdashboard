# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    # The flowviz migration creates the table by renaming the old one.
    dependencies = [
        ('flowviz', '0013_rename_watershed_table')
    ]

    # The migration we depend on created the table by renaming the old table,
    # so we just need to apply the state change.
    state_operations = [
        migrations.CreateModel(
            name='Watershed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations = state_operations)
    ]
