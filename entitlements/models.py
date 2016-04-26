from __future__ import unicode_literals

from django.db import models

from forms import DayOfYearFormField

import re

class DayOfYear(object):
    def __init__(self, month, day):
        self.month = month
        self.day = day

    def __str__(self):
        return "{:0>2}-{:0>2}".format(self.month, self.day)

class DayOfYearField(models.Field):
    """A custom form field to represent a day of the year as a
    month and day.
    """
    date_pattern = DayOfYearFormField.date_pattern

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 5
        super(DayOfYearField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(DayOfYearField, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def _parse(self, value):
        match = re.match(self.date_pattern, value)
        if not match:
            raise models.ValidationError("Invalid day of year formatting in database.")
        return DayOfYear(int(match.group('month')), int(match.group('day')))

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return self._parse(value)

    def to_python(self, value):
        if isinstance(value, DayOfYear):
            return value
        if value is None:
            return value
        return self._parse(value)

    def get_prep_value(self, value):
        return str(value)

    def formfield(self, formclass=DayOfYearFormField, **kwargs):
        return formclass(**kwargs)

    def get_internal_type(self):
        return 'CharField'


        

class SecurityRanking(models.Model):
    name = models.CharField(max_length=40)
    order = models.IntegerField(default=100)

    def __unicode__(self):
        return self.name

class PermanenceRanking(models.Model):
    name = models.CharField(max_length=40)
    order = models.IntegerField(default=100)

    def __unicode__(self):
        return self.name

class EntitlementSet(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()

    def __unicode__(self):
        return self.name

class Entitlement(models.Model):
    entitlement_set = models.ForeignKey(EntitlementSet)
    name = models.CharField(max_length=120)

    security = models.ForeignKey(SecurityRanking)
    permanence = models.ForeignKey(PermanenceRanking)

    priority_date = models.DateField(help_text="The priority date of the entitlement.")
    effective_date = models.DateField(help_text="The date on which the entitlement becomes effective.")
    term = models.IntegerField(help_text="The term of the entitlement in years.")

    flow_rate = models.FloatField(help_text="The flow rate of the entitlement in CFS.")
    begin = DayOfYearField(help_text="Month/Day on which the entitlement begins each year.")
    end = DayOfYearField(help_text="Month/Day on which the entitlement ends each year.")

    def __unicode__(self):
        return self.name

    
