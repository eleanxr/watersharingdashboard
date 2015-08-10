from django.db import models

from django.contrib.auth.models import User

import datetime

from waterkit import rasterflow, usgs_data

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

class DataFile(models.Model):
    data_file = models.FileField(upload_to='data-files')
    name = models.CharField(max_length=80)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

class Project(models.Model):
    watershed = models.ForeignKey(Watershed)
    name = models.CharField(max_length=NAME_LIMIT)
    description = models.TextField()

    def __unicode__(self):
        return self.name

class CyclicTarget(models.Model):
    name = models.CharField(max_length=NAME_LIMIT)
    description = models.TextField()

    def __unicode__(self):
        return self.name

class Scenario(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=NAME_LIMIT)
    description = models.TextField()

    attribute_name = models.CharField(max_length=NAME_LIMIT, default="Flow")
    attribute_units = models.CharField(max_length=NAME_LIMIT, default="Cubic Feet per Second")
    attribute_units_abbr = models.CharField(max_length=10, default="cfs")

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
    excel_file = models.ForeignKey(DataFile, null=True, blank=True)
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
            data = rasterflow.read_data(
                self.gage_location.identifier,
                self.start_date, self.end_date,
                target_data)
            return data
        elif self.source_type == self.SOURCE_EXCEL:
            data = rasterflow.read_excel_data(
                self.excel_file.data_file,
                self.date_column_name,
                self.attribute_column_name,
                self.sheet_name,
                self.target_column_name
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
            return self.target_column_name

    def get_gap_attribute_name(self):
        if self.source_type == self.SOURCE_GAGE:
            return self.parameter_name + "-gap"
        else:
            return self.attribute_column_name + "-gap"



class CyclicTargetElement(models.Model):
    target = models.ForeignKey(CyclicTarget)
    from_month = models.IntegerField()
    from_day = models.IntegerField()
    to_month = models.IntegerField()
    to_day = models.IntegerField()
    target_value = models.DecimalField(max_digits=8, decimal_places=2)

    def __unicode__(self):
        params = (
            self.flow_target.name,
            self.from_month,
            self.from_day,
            self.to_month,
            self.to_day,
            self.target_value
        )
        return '%s: From %d-%d to %d-%d at %f' % params
