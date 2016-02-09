# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0008_auto_20160208_1726'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectScenarioRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.ForeignKey(to='flowviz.Project')),
                ('scenario', models.ForeignKey(to='flowviz.Scenario')),
            ],
        ),
    ]
