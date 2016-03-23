from django.db import models

from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

import datetime

from waterkit.flow import rasterflow, usgs_data
from utils import cache_data

import datafiles.models as datafiles
import watersheds.models as watersheds
import scenarios.models as scenarios

import logging
logger = logging.getLogger(__name__)

NAME_LIMIT = 80
DESCRIPTION_LIMIT = 1000

def begin_default():
    return datetime.date(1950, 01, 01)

def end_default():
    return datetime.date(2014, 12, 31)

class Project(models.Model):
    watershed = models.ForeignKey(watersheds.Watershed)
    name = models.CharField(max_length=NAME_LIMIT)
    description = models.TextField()
    # TODO Add validator to check value.
    huc_scale = models.IntegerField(null=True, blank=True)

    scenarios = models.ManyToManyField(
        scenarios.Scenario, through='ProjectScenarioRelationship')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project_detail', args=[str(self.id)])

class HUCRegion(models.Model):
    project = models.ForeignKey(Project)
    hucid = models.CharField(max_length=12)

    def __unicode__(self):
        return self.hucid

class GISLayer(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=NAME_LIMIT)
    description = models.TextField()
    url = models.URLField()

    def __unicode__(self):
        return self.name

class ProjectScenarioRelationship(models.Model):
    project = models.ForeignKey(Project)
    scenario = models.ForeignKey(scenarios.Scenario)
