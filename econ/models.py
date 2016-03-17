from django.db import models

from django.core.urlresolvers import reverse

from waterkit.econ import analysis

class ApiKey(models.Model):
    name = models.CharField(max_length=80)
    system = models.CharField(max_length=10)
    key = models.CharField(max_length=80)
    use_key = models.BooleanField(default=False)

    def __unicode(self):
        return "%s: %s" % (self.system, self.name)

class CropMix(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(null=True)
    state = models.CharField(max_length=2)
    county = models.CharField(max_length=40)
    source = models.CharField(max_length=20, default='CENSUS')
    cpi_adjustment_year = models.IntegerField()

    def get_absolute_url(self):
        return reverse('crop_mix_detail', args=[str(self.id)])

    def __unicode__(self):
        return self.name

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
