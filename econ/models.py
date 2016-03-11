from django.db import models

from django.core.urlresolvers import reverse

class ApiKey(models.Model):
    name = models.CharField(max_length=80)
    system = models.CharField(max_length=10)
    key = models.CharField(max_length=80)
    use_key = models.BooleanField(default=False)

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

class CropMixCommodity(models.Model):
    analysis = models.ForeignKey(CropMix)
    commodity = models.CharField(max_length=80)
