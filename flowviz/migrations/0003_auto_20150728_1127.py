# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import flowviz.models


class Migration(migrations.Migration):

    dependencies = [
        ('flowviz', '0002_gagelocation_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradedflowtarget',
            name='begin_date',
            field=models.DateField(default=flowviz.models.begin_default),
        ),
        migrations.AddField(
            model_name='gradedflowtarget',
            name='end_date',
            field=models.DateField(default=flowviz.models.end_default),
        ),
    ]
