# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0015_delete_watershed'),
    ]

    state_operations = [
    ]

    database_operations = [
        migrations.AlterModelTable('Scenario', 'scenarios_scenario'),
        migrations.AlterModelTable('GageLocation', 'scenarios_gagelocation'),
        migrations.AlterModelTable('CyclicTarget', 'scenarios_cyclictarget'),
        migrations.AlterModelTable('CyclicTargetElement', 'scenarios_cyclictargetelement')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=state_operations,
            database_operations=database_operations
        )
    ]
