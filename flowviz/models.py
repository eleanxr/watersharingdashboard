from django.db import models

from django.contrib.auth.models import User

import datetime

from waterkit import rasterflow

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

class GradedFlowTarget(models.Model):
    watershed = models.ForeignKey(Watershed)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name

class DataFile(models.Model):
    data_file = models.FileField(upload_to='data-files')
    name = models.CharField(max_length=80)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

class GageDataSource(models.Model):
    gage_location = models.ForeignKey(GageLocation)
    start_date = models.DateField(default=begin_default)
    end_date = models.DateField(default=end_default)
    graded_flow_target = models.ForeignKey(GradedFlowTarget)

    def __unicode__(self):
        return "%s: %s to %s" % (self.gage_location, self.start_date, self.end_date)

class ExcelDataSource(models.Model):
    excel_file = models.ForeignKey(DataFile)
    sheet_name = models.CharField(max_length=80)
    date_column_name = models.CharField(max_length=80)
    flow_column_name = models.CharField(max_length=80)
    target_column_name = models.CharField(max_length=80)

    def __unicode__(self):
        return "%s:%s" % (self.excel_file, self.sheet_name)

class Scenario(models.Model):
    watershed = models.ForeignKey(Watershed)
    name = models.CharField(max_length=NAME_LIMIT)
    description = models.TextField()

    SOURCE_GAGE = "GAGE"
    SOURCE_EXCEL = "XLSX"
    SOURCE_CHOICES = [
        (SOURCE_GAGE, "USGS Gage"),
        (SOURCE_EXCEL, "Excel File"),
    ]
    source_type = models.CharField(max_length=4, choices=SOURCE_CHOICES,
        default=SOURCE_GAGE)

    gage_data = models.ForeignKey(GageDataSource, null=True, blank=True)
    excel_data = models.ForeignKey(ExcelDataSource, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_data(self):
        if self.source_type == self.SOURCE_GAGE:
            target_data = rasterflow.GradedFlowTarget()
            for element in self.gage_data.graded_flow_target.gradedflowtargetelement_set.all():
                fr = "%d-%d" % (element.from_month, element.from_day)
                to = "%d-%d" % (element.to_month, element.to_day)
                target_data.add((fr, to), float(element.target_value))
            data = rasterflow.read_data(
                self.gage_data.gage_location.identifier,
                self.gage_data.start_date, self.gage_data.end_date,
                target_data)
            return data
        elif self.source_type == self.SOURCE_EXCEL:
            data = rasterflow.read_excel_data(
                self.excel_data.excel_file.data_file,
                self.excel_data.date_column_name,
                self.excel_data.flow_column_name,
                self.excel_data.sheet_name,
                self.excel_data.target_column_name
            )
            return data
        else:
            return None



class GradedFlowTargetElement(models.Model):
    flow_target = models.ForeignKey(GradedFlowTarget)
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
