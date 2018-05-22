from __future__ import unicode_literals

from django.db import models
from datetime import datetime



class Crawl(models.Model):
	STATUS_CHOICES = (
        (1, 'Started'),
        (2, 'Inprogress'),
        (3, 'Success'),
        (4, 'Failed'),
    )
	uid = models.CharField(max_length = 50)
	url = models.URLField()
	created_time = models.DateTimeField(default = datetime.now)
	started_time = models.DateTimeField(default = datetime.now)
	finished_time = models.DateTimeField(null=True,blank = True)
	status = models.IntegerField(default = 1)
	description  = models.CharField(null = True,blank = True,max_length = 100);
	error = models.CharField(null = True,blank = True,max_length = 200)


class Image(models.Model):
	image_url = models.URLField()
	created_time = models.DateTimeField(default = datetime.now)
	crawl = models.ForeignKey(Crawl)
