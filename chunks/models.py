from django.db import models

# Create your models here.
class Chunk(models.Model):
	name = models.CharField(max_length=255, unique=True)
	content = models.TextField(blank=True)
	
	published = models.DateTimeField('Date published', auto_now_add=True)
	updated = models.DateTimeField('Date updated', auto_now=True, auto_now_add=True)
	
	def __unicode__(self):
		return self.name
