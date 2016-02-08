# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0007_auto_20160208_1646'),
    ]

    # State change only, the database table was renamed earlier
    state_operations = [
        migrations.DeleteModel(name = 'DataFile')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations = state_operations)
    ]
