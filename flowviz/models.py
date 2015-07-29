from django.db import models

import datetime

# Create your models here.
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
    location = models.ForeignKey(GageLocation)
    name = models.CharField(max_length=200)
    begin_date = models.DateField(default=begin_default)
    end_date = models.DateField(default=end_default)
    
    def __unicode__(self):
        return self.name
    
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
    