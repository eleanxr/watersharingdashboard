from django.db import models

from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

import datetime

from waterkit import rasterflow, usgs_data
import cache_data

import datafiles.models as datafiles

import logging
logger = logging.getLogger(__name__)

NAME_LIMIT = 80
DESCRIPTION_LIMIT = 1000

class Watershed(models.Model):
    name = models.CharField(max_length = 200)

    def __unicode__(self):
        return self.name

class GageLocation(models.Model):
    watershed = models.ForeignKey(Watershed)
    identifier = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s: %s" % (self.identifier, self.description)

def begin_default():
    return datetime.date(1950, 01, 01)

def end_default():
    return datetime.date(2014, 12, 31)

class CyclicTarget(models.Model):
    name = models.CharField(max_length=NAME_LIMIT)
    description = models.TextField()

    def __unicode__(self):
        return self.name

class Scenario(models.Model):
    name = models.CharField(max_length=NAME_LIMIT)
    description = models.TextField()

    attribute_multiplier = models.FloatField(default=1.0,
        help_text="Input flow data must be reported in cubic feet per second (CFS). If your data is not already in CFS, then use this field to set the a multiplication value that will convert your data to CFS.")

    SOURCE_GAGE = "GAGE"
    SOURCE_EXCEL = "XLSX"
    SOURCE_CHOICES = [
        (SOURCE_GAGE, "USGS Gage"),
        (SOURCE_EXCEL, "Excel File"),
    ]
    source_type = models.CharField(max_length=4, choices=SOURCE_CHOICES,
        default=SOURCE_GAGE)

    # Gage data source.
    gage_location = models.ForeignKey(GageLocation, null=True, blank=True)
    parameter_code = models.CharField(max_length="10", default=usgs_data.FLOW_PARAMETER_CODE,
        null=True, blank=True)
    parameter_name = models.CharField(max_length="20", default="flow")
    start_date = models.DateField(default=begin_default, null=True, blank=True)
    end_date = models.DateField(default=end_default, null=True, blank=True)
    target = models.ForeignKey(CyclicTarget, null=True, blank=True)

    # Excel data source.
    excel_file = models.ForeignKey(datafiles.DataFile, null=True, blank=True)
    sheet_name = models.CharField(max_length=80, null=True, blank=True)
    date_column_name = models.CharField(max_length=80, null=True, blank=True)
    attribute_column_name = models.CharField(max_length=80, null=True, blank=True)
    target_column_name = models.CharField(max_length=80, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_data(self):
        if self.source_type == self.SOURCE_GAGE:
            target_data = rasterflow.GradedFlowTarget()
            for element in self.target.cyclictargetelement_set.all():
                fr = "%d-%d" % (element.from_month, element.from_day)
                to = "%d-%d" % (element.to_month, element.to_day)
                target_data.add((fr, to), float(element.target_value))
            data = cache_data.read_usgs_data(
                self.gage_location.identifier,
                self.start_date, self.end_date,
                target_data, self.attribute_multiplier)
            return data
        elif self.source_type == self.SOURCE_EXCEL:
            data = cache_data.read_excel_data(
                self.excel_file.data_file,
                self.date_column_name,
                self.attribute_column_name,
                self.sheet_name,
                self.target_column_name,
                self.attribute_multiplier
            )
            return data
        else:
            return None

    def get_attribute_name(self):
        if self.source_type == self.SOURCE_GAGE:
            return self.parameter_name
        else:
            return self.attribute_column_name

    def get_target_attribute_name(self):
        if self.source_type == self.SOURCE_GAGE:
            return self.parameter_name + "-target"
        else:
            return self.attribute_column_name + "-target"

    def get_gap_attribute_name(self):
        if self.source_type == self.SOURCE_GAGE:
            return self.parameter_name + "-gap"
        else:
            return self.attribute_column_name + "-gap"

    def get_absolute_url(self):
        return reverse('scenario', args=[str(self.id)])


class CyclicTargetElement(models.Model):
    target = models.ForeignKey(CyclicTarget)
    from_month = models.IntegerField()
    from_day = models.IntegerField()
    to_month = models.IntegerField()
    to_day = models.IntegerField()
    target_value = models.DecimalField(max_digits=8, decimal_places=2)

    def __unicode__(self):
        params = (
            self.target.name,
            self.from_month,
            self.from_day,
            self.to_month,
            self.to_day,
            self.target_value
        )
        return '%s: From %d-%d to %d-%d at %f' % params

class Project(models.Model):
    watershed = models.ForeignKey(Watershed)
    name = models.CharField(max_length=NAME_LIMIT)
    description = models.TextField()
    # TODO Add validator to check value.
    huc_scale = models.IntegerField(null=True, blank=True)

    scenarios = models.ManyToManyField(
        Scenario, through='ProjectScenarioRelationship')

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
    scenario = models.ForeignKey(Scenario)
