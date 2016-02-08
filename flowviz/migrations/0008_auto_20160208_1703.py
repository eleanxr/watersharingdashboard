# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0006_gislayer'),
    ]

    database_operations = [
        migrations.AlterModelTable('DataFile', 'datafiles_datafile')
    ]

    state_operations = []

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations = database_operations,
            state_operations = state_operations
        )
    ]
