from django.db import models

from django.core.urlresolvers import reverse

import datafiles.models as datafiles

from waterkit.econ import analysis, usda_data

import pandas as pd

class ApiKey(models.Model):
    SYSTEM_CHOICES = [
        ("USDA NASS", "USDA NASS"),
        ("BLS", "Bureau of Labor Statistics"),
    ]
    name = models.CharField(max_length=80)
    system = models.CharField(max_length=10, choices=SYSTEM_CHOICES)
    key = models.CharField(max_length=80)
    use_key = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s: %s" % (self.system, self.name)

def create_nass_client():
    keys = ApiKey.objects.filter(use_key = True, system = "USDA NASS")
    if not keys:
        raise Exception("No USDA NASS API keys have been configured.")
    return usda_data.NASSDataSource(keys[0].key)

class CropMix(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(null=True)
    state = models.CharField(max_length=2)
    county = models.CharField(max_length=40)

    DATA_SOURCES = [
        ('CENSUS', 'Census'),
        ('SURVEY', 'Survey'),
    ]
    source = models.CharField(max_length=20, default='CENSUS',
        choices=DATA_SOURCES)
    cpi_adjustment_year = models.IntegerField(
        verbose_name="CPI adjustment year",
        help_text="Adjust crop prices using the consumer price index for the given year."
    )

    SOURCE_NASS = "NASS"
    SOURCE_EXCEL = "XLSX"
    SOURCE_CHOICES = [
        (SOURCE_NASS, "USDA NASS"),
        (SOURCE_EXCEL, "Excel File"),
    ]
    source_type = models.CharField(max_length=4, choices=SOURCE_CHOICES,
        default=SOURCE_NASS, help_text="Crop mix data source")

    # Excel data
    excel_file = models.ForeignKey(datafiles.DataFile, null=True, blank=True,
        help_text="Upload an Excel spreadsheet to provide agriculture data.")
    sheet_name = models.CharField(max_length=80, null=True, blank=True,
        help_text="The name of the worksheet in the Excel file containing the crop data.")
    year_column_name = models.CharField(max_length=80, null=True, blank=True,
        help_text="The name of the column specifying the year of each measurement.")
    crop_column_name = models.CharField(max_length=80, null=True, blank=True,
        help_text="The name of the column specifying which crop is being measured.")
    unit_column_name = models.CharField(max_length=80, null=True, blank=True,
        help_text="The name of the column specifying the unit of measurement.")

    def get_absolute_url(self):
        return reverse('crop_mix_detail', args=[str(self.id)])

    def __unicode__(self):
        return self.name

    def get_data(self):
        years = map(lambda y: y.year, self.cropmixyear_set.all())
        commodities = map(lambda c: c.commodity, self.cropmixcommodity_set.all())
        production_practices = map(lambda p: p.production_practice,
            self.cropmixproductionpractice_set.all())
        if self.source_type == CropMix.SOURCE_NASS:
            connection = create_nass_client()
            data = analysis.NASSCropMixDataSet(
                connection,
                self.state,
                self.county,
                years,
                commodities,
                production_practices=production_practices
            )
        elif self.source_type == CropMix.SOURCE_EXCEL:
            data = analysis.ExcelCropMixDataSet(
                self.excel_file.data_file,
                sheetname = self.sheet_name,
                year_column = self.year_column_name,
                crop_column = self.crop_column_name,
                unit_column = self.unit_column_name
            )
        else:
            raise Exception("Unknown crop mix data source.")
        return data, years, commodities

class CropMixYear(models.Model):
    analysis = models.ForeignKey(CropMix)
    year = models.IntegerField()

    def __unicode__(self):
        return str(self.year)

class CropMixCommodity(models.Model):
    analysis = models.ForeignKey(CropMix)
    commodity = models.CharField(max_length=80)

    def __unicode__(self):
        return self.commodity

class CropMixProductionPractice(models.Model):
    analysis = models.ForeignKey(CropMix)
    production_practice = models.CharField(max_length=80)

    def __unicode__(self):
        return self.production_practice

class CropMixGroup(models.Model):
    analysis = models.ForeignKey(CropMix)
    group_name = models.CharField(max_length=80)
    revenue = models.FloatField(
        help_text="Revenue estimate in $/acre"
    )
    labor = models.FloatField(
        help_text="Required labor in hours/acre"
    )
    niwr = models.FloatField(
        default=0.0,
        help_text="Net irrigation water requirement in ft/acre",
    )

    def as_cropgroup(self):
        """Get the group as an analysis.CropGroup."""
        return analysis.CropGroup(
            self.group_name,
            self.revenue,
            self.labor,
            self.niwr,
            map(lambda i: i.item_name, self.cropmixgroupitem_set.all())
        )

    def __unicode__(self):
        return "%s: %s" % (self.analysis.name, self.group_name)

class CropMixGroupItem(models.Model):
    group = models.ForeignKey(CropMixGroup)
    item_name = models.CharField(max_length=80)

    def __unicode__(self):
        return self.item_name

class ConsumerPriceIndexData(models.Model):
    year = models.IntegerField()
    value = models.FloatField()

    def __unicode__(self):
        return "(%d, %f)" % (self.year, self.value)

    @staticmethod
    def as_dataframe():
        data = ConsumerPriceIndexData.objects.all()
        return pd.Series(
            map(lambda data: data.value, data),
            map(lambda data: data.year, data)
        )
