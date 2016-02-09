# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0011_remove_scenario_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='scenarios',
            field=models.ManyToManyField(to='flowviz.Scenario', through='flowviz.ProjectScenarioRelationship'),
        ),
    ]
