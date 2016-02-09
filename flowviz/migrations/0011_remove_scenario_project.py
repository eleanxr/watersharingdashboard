# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0010_scenario_rel_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scenario',
            name='project',
        ),
    ]
