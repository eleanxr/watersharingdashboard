# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    # Depends additionally on the creation of the scenarios app model.
    dependencies = [
        ('flowviz', '0016_rename_scenario_tables'),
        ('scenarios', '0001_initial')
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='scenarios',
            field=models.ManyToManyField(to='scenarios.Scenario', through='flowviz.ProjectScenarioRelationship'),
        ),
        migrations.AlterField(
            model_name='projectscenariorelationship',
            name='scenario',
            field=models.ForeignKey(to='scenarios.Scenario'),
        ),
    ]
