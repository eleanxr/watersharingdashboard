# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        # This migration depends on the migration that renames
        # the datafiles database table in the flowviz app.
        ('flowviz', '0008_auto_20160208_1703'),
    ]

    # The migration we depend on created the tables, so we only apply the state
    # operations here. We're using the table that was renamed.
    state_operations = [
        migrations.CreateModel(
            name='DataFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_file', models.FileField(upload_to=b'data-files')),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField()),
                ('uploaded_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations = state_operations)
    ]
