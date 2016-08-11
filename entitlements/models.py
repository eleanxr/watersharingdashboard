from __future__ import unicode_literals

from django.db import models

from utils.modelfields import DayOfYearField

from waterkit.flow import rasterflow
import pandas as pd

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

    def as_daily_dataframe(self, begin_date, end_date):
        entitlements = {}
        for entitlement in self.entitlement_set.all():
            target = rasterflow.GradedFlowTarget()
            start_day = pd.Timestamp(str(entitlement.begin) + "-2000").dayofyear
            end_day = pd.Timestamp(str(entitlement.end) + "-2000").dayofyear
            target.add_by_dayofyear((start_day, end_day), entitlement.flow_rate)
            entitlements[entitlement.name] = target.as_daily_timeseries(
                begin_date, end_date,
                entitlement.effective_date, entitlement.term
            )
        return pd.DataFrame(entitlements)

    def rates_by_security(self, begin_date, end_date):
        result = {}
        for security_ranking in SecurityRanking.objects.all().order_by('order'):
            entitlements = {}
            for entitlement in self.entitlement_set.filter(security=security_ranking):
                target = rasterflow.GradedFlowTarget()
                start_day = pd.Timestamp(str(entitlement.begin) + "-2000").dayofyear
                end_day = pd.Timestamp(str(entitlement.end) + "-2000").dayofyear
                target.add_by_dayofyear((start_day, end_day), entitlement.flow_rate)
                entitlements[entitlement.name] = target.as_daily_timeseries(
                    begin_date, end_date,
                    entitlement.effective_date, entitlement.term
                )
            result[security_ranking.name] = pd.DataFrame(entitlements).sum(axis=1)
        return pd.DataFrame(result)

    def rates_by_permanence(self, begin_date, end_date):
        result = {}
        for permanence_ranking in PermanenceRanking.objects.all().order_by('order'):
            entitlements = {}
            for entitlement in self.entitlement_set.filter(permanence=permanence_ranking):
                target = rasterflow.GradedFlowTarget()
                start_day = pd.Timestamp(str(entitlement.begin) + "-2000").dayofyear
                end_day = pd.Timestamp(str(entitlement.end) + "-2000").dayofyear
                target.add_by_dayofyear((start_day, end_day), entitlement.flow_rate)
                entitlements[entitlement.name] = target.as_daily_timeseries(
                    begin_date, end_date,
                    entitlement.effective_date, entitlement.term
                )
            result[permanence_ranking.name] = pd.DataFrame(entitlements).sum(axis=1)
        return pd.DataFrame(result)

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
