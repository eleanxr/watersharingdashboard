# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    # This migration depends on the rename in 0008_auto_2016_0208_1703 and on
    # the state change in datafiles, 0001_initial.
    dependencies = [
        ('flowviz', '0008_auto_20160208_1703'),
        ('datafiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='excel_file',
            field=models.ForeignKey(blank=True, to='datafiles.DataFile', null=True),
        ),

        # Don't delete the model, we renamed it in 0008_auto_2016_0208_1703 so
        # the data could be used by the new datafiles application.
        # migrations.DeleteModel(
        #    name='DataFile',
        #),
    ]
