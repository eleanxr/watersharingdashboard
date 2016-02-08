from django.db import models
from django.contrib.auth.models import User

class DataFile(models.Model):
    data_file = models.FileField(upload_to='data-files')
    name = models.CharField(max_length=80)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.name
