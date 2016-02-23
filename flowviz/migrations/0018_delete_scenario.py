# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0017_repoint_scenarios'),
    ]

    # The actual database tables were renamed. This just deletes them from them
    # Django model.
    state_operations = [
        migrations.RemoveField(
            model_name='cyclictargetelement',
            name='target',
        ),
        migrations.RemoveField(
            model_name='gagelocation',
            name='watershed',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='excel_file',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='gage_location',
        ),
        migrations.RemoveField(
            model_name='scenario',
            name='target',
        ),
        migrations.DeleteModel(
            name='CyclicTarget',
        ),
        migrations.DeleteModel(
            name='CyclicTargetElement',
        ),
        migrations.DeleteModel(
            name='GageLocation',
        ),
        migrations.DeleteModel(
            name='Scenario',
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
