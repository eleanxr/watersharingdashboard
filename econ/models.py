from django.db import models

class NASSApiKey(models.Model):
    name = models.CharField(max_length=80)
    key = models.CharField(max_length=80)
    use_key = models.BooleanField(default=False)

class CropMix(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(null=True)
    state = models.CharField(max_length=2)
    county = models.CharField(max_length=40)
    source = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class CropMixYear(models.Model):
    analysis = models.ForeignKey(CropMix)
    year = models.IntegerField()

class CropMixCommodity(models.Model):
    analysis = models.ForeignKey(CropMix)
    commodity = models.CharField(max_length=80)
