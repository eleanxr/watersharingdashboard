# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0014_repoint_watersheds'),
    ]

    # The deletion of the model is a state operation only since the database
    # table was relocated to a new application.
    state_operations = [
        migrations.DeleteModel(
            name='Watershed',
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
