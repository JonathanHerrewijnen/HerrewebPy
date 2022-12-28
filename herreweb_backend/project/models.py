from django.db import models
from herreweb_backend.utils import *

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default="No description added")
    status = models.IntegerField(default=ProjectStatus.RUNNING)
    image = models.ImageField(null=True, blank=True)
    rtd_url = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    visible = models.BooleanField(default=False)

    def _str_(self):
        return self.title
