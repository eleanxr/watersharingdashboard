from __future__ import unicode_literals

from django.db import models

from utils.modelfields import DayOfYearField

import re

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
    begin = DayOfYearField(
        verbose_name="Begin Day",
        help_text="Month/Day on which the entitlement begins each year."
    )
    end = DayOfYearField(
        verbose_name="End Day",
        help_text="Month/Day on which the entitlement ends each year."
    )

    def __unicode__(self):
        return self.name
