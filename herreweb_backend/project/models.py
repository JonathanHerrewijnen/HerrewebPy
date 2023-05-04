from django.db import models
from herreweb_backend.utils import *

import os
from uuid import uuid4

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default="No description added")
    status = models.IntegerField(default=ProjectStatus.RUNNING)
    image = models.ImageField(upload_to=path_and_rename("static/project_images/"), null=True, blank=True)
    rtd_url = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    visible = models.BooleanField(default=False)

    def _str_(self):
        return self.title
