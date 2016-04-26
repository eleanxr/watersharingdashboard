from django.db import models

from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

import datetime

from waterkit.flow import rasterflow, usgs_data
from utils import cache_data

import datafiles.models as datafiles
import watersheds.models as watersheds
import scenarios.models as scenarios
import econ.models as econ

import logging
logger = logging.getLogger(__name__)

NAME_LIMIT = 80
DESCRIPTION_LIMIT = 1000

def begin_default():
    return datetime.date(1950, 01, 01)

def end_default():
    return datetime.date(2014, 12, 31)

class Project(models.Model):
    watershed = models.ForeignKey(watersheds.Watershed, help_text="The watershed in which this project operates.")
    name = models.CharField(max_length=NAME_LIMIT, help_text="Choose a name for this project.")
    description = models.TextField(help_text="Briefly describe this project.")

    HUC_CHOICES = [
        (2, "HUC-2"),
        (4, "HUC-4"),
        (6, "HUC-6"),
        (8, "HUC-8"),
        (10, "HUC-10"),
        (12, "HUC-12"),
    ]

    huc_scale = models.IntegerField(null=True, blank=True, choices=HUC_CHOICES,
        help_text="Choose a HUC scale for the basin this project operates in.")

    scenarios = models.ManyToManyField(
        scenarios.Scenario, through='ProjectScenarioRelationship'
    )
    crop_mixes = models.ManyToManyField(
        econ.CropMix, through='ProjectCropMixRelationship'
    )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project_detail', args=[str(self.id)])

class HUCRegion(models.Model):
    project = models.ForeignKey(Project)
    hucid = models.CharField(max_length=12, help_text="Choose a HUC ID for the project.")

    def __unicode__(self):
        return self.hucid

class GISLayer(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=NAME_LIMIT, help_text="Choose a name for this layer.")
    description = models.TextField(help_text="Briefly describe this layer.")
    url = models.URLField(help_text="Set the URL where the layer is hosted.")

    def __unicode__(self):
        return self.name

class ProjectScenarioRelationship(models.Model):
    project = models.ForeignKey(Project)
    scenario = models.ForeignKey(scenarios.Scenario)

    def __unicode__(self):
        return "%s - %s" % (self.project.name, self.scenario.name)
        
class ProjectCropMixRelationship(models.Model):
    project = models.ForeignKey(Project)
    crop_mix = models.ForeignKey(econ.CropMix)
    
    def __unicode__(self):
        return "%s - %s" % (self.project.name, self.crop_mix.name)
