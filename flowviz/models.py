from django.db import models

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

class Scenario(models.Model):
    watershed = models.ForeignKey(Watershed)
    name = models.CharField(max_length=NAME_LIMIT)
    description = models.CharField(max_length=DESCRIPTION_LIMIT)
    
    # Flow target.
    flow_target = models.ForeignKey(GradedFlowTarget)
    
    # Optional - use a gage or a custom data file.
    gage_location = models.ForeignKey(GageLocation, null=True, blank=True)
    start_date = models.DateField(default=begin_default, null=True, blank=True)
    end_date = models.DateField(default=end_default, null=True, blank=True)
    # OR
    flow_data_file = models.FileField(null=True, blank=True)
    date_column_name = models.CharField(max_length=80, null=True, blank=True)
    flow_column_name = models.CharField(max_length=80, null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
    def get_data(self):
        target_data = rasterflow.GradedFlowTarget()
        for element in self.flow_target.gradedflowtargetelement_set.all():
            fr = "%d-%d" % (element.from_month, element.from_day)
            to = "%d-%d" % (element.to_month, element.to_day)
            target_data.add((fr, to), float(element.target_value))
        
        data = rasterflow.read_data(
            self.gage_location.identifier,
            self.start_date, self.end_date,
            target_data)
        return data

    

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
    