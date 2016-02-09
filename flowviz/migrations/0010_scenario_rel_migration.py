# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def migrate_scenarios(apps, schema_editor):
    """Migrates many-to-one scenario-project relationships into
    many to many project-scenario relationships.
    """
    Scenario = apps.get_model('flowviz', 'Scenario')
    ProjectScenarioRelationship = apps.get_model('flowviz', 'ProjectScenarioRelationship')

    for scenario in Scenario.objects.all():
        relationship = ProjectScenarioRelationship()
        relationship.project_id = scenario.project_id
        relationship.scenario_id = scenario.id
        relationship.save()

class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0009_projectscenariorelationship'),
    ]

    operations = [
        migrations.RunPython(migrate_scenarios)
    ]
