from django.db import models

import watersheds.models as watersheds
import datafiles.models as datafiles
import econ.models as econ
import entitlements.models as entitlements

from waterkit.flow import usgs_data, rasterflow

from utils import cache_data
from utils.modelfields import DayOfYearField

from django.core.urlresolvers import reverse

from django.core.validators import MinValueValidator, MaxValueValidator

from datetime import datetime
import calendar

NAME_LIMIT = 80

class GageLocation(models.Model):
    watershed = models.ForeignKey(watersheds.Watershed)
    identifier = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s: %s" % (self.identifier, self.description)

def begin_default():
    return datetime(1950, 1, 1).date()

def end_default():
    return datetime(2014, 12, 31).date()

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

    drought_exceedance = models.IntegerField(
        default=90,
        help_text="Water volume exceedance percent value to identify drought years.",
        validators = [
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )

    # Critical Season Fields.
    critical_season_begin = DayOfYearField(
        help_text="Day on which the critical season to measure starts (MM-DD).",
        null=True,
        blank=True
    )
    critical_season_end = DayOfYearField(
        null=True,
        blank=True,
        help_text="Day on which the critical season to measure ends (MM-DD)."
    )

    # Gage data source.
    gage_location = models.ForeignKey(GageLocation, null=True, blank=True)
    parameter_code = models.CharField(max_length=10, default=usgs_data.FLOW_PARAMETER_CODE,
        null=True, blank=True)
    parameter_name = models.CharField(max_length=20, default="flow")
    start_date = models.DateField(default=begin_default, null=True, blank=True)
    end_date = models.DateField(default=end_default, null=True, blank=True)

    # Excel data source.
    excel_file = models.ForeignKey(datafiles.DataFile, null=True, blank=True)
    sheet_name = models.CharField(max_length=80, null=True, blank=True)
    date_column_name = models.CharField(max_length=80, null=True, blank=True)
    attribute_column_name = models.CharField(max_length=80, null=True, blank=True)
    target_column_name = models.CharField(max_length=80, null=True, blank=True)

    # Agricultural data.
    crop_mix = models.ForeignKey(econ.CropMix, null=True, blank=True,
        help_text="Choose a crop mix to use as an agricultural data source for this scenario.")

    # Instream flow rights.
    instream_flow_rights = models.ForeignKey(entitlements.EntitlementSet,
        null=True, blank=True,
        help_text="Choose a set of instream flow rights that apply to this scenario.")

    def __unicode__(self):
        return self.name

    def get_data(self):
        if self.critical_season_begin and self.critical_season_end:
            critical_season = (
                str(self.critical_season_begin),
                str(self.critical_season_end)
            )
        else:
            critical_season = None
        if self.source_type == self.SOURCE_GAGE:
            target_data = rasterflow.GradedFlowTarget()
            elements = self.cyclictargetelement_set.all()
            for element in elements:
                fr = "%d-%d" % (element.from_month, element.from_day)
                to = "%d-%d" % (element.to_month, element.to_day)
                target_data.add((fr, to), float(element.target_value))
            data = cache_data.read_usgs_data(
                self.gage_location.identifier,
                self.start_date,
                self.end_date,
                target_data,
                self.attribute_multiplier,
                critical_season
            )
            return data
        elif self.source_type == self.SOURCE_EXCEL:
            data = cache_data.read_excel_data(
                self.excel_file.data_file,
                self.date_column_name,
                self.attribute_column_name,
                self.sheet_name,
                self.target_column_name,
                self.attribute_multiplier,
                critical_season
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
    MONTHS = [(i, calendar.month_name[i]) for i in range(1, 13)]
    DAY_VALIDATORS = [
        MinValueValidator(1),
        MaxValueValidator(31)
    ]

    scenario = models.ForeignKey(Scenario)
    from_month = models.IntegerField(choices=MONTHS)
    from_day = models.IntegerField(validators=DAY_VALIDATORS)
    to_month = models.IntegerField(choices=MONTHS)
    to_day = models.IntegerField(validators=DAY_VALIDATORS)
    target_value = models.DecimalField(max_digits=8, decimal_places=2)

    def __unicode__(self):
        params = (
            self.scenario.name,
            self.from_month,
            self.from_day,
            self.to_month,
            self.to_day,
            self.target_value
        )
        return '%s: From %d-%d to %d-%d at %f' % params
