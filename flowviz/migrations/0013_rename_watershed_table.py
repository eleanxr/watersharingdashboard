# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0012_add_project_scenarios_field'),
    ]

    state_operations = []

    database_operations = [
        migrations.AlterModelTable('Watershed', 'watersheds_watershed')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations = database_operations,
            state_operations = state_operations
        )
    ]
