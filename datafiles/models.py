from django.db import models
from django.contrib.auth.models import User

class DataFile(models.Model):
    data_file = models.FileField(upload_to='data-files')
    name = models.CharField(max_length=80)
    description = models.TextField()

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Spatial location of data (if applicable)"
    )
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Spatial location of data (if applicable)"
    )

    uploaded_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.name
