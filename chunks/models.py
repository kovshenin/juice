from django.db import models
from juice.front.shortcodes import shortcodes

# Create your models here.
class Chunk(models.Model):
	name = models.CharField(max_length=255, unique=True)
	content = models.TextField(blank=True)
	
	published = models.DateTimeField('Date published', auto_now_add=True)
	updated = models.DateTimeField('Date updated', auto_now=True, auto_now_add=True)
	
	def __unicode__(self):
		return self.name

class ChunksAPI():
	@staticmethod
	def shortcode(kwargs):
		chunk_name = kwargs.get("name").__str__()
		chunk = Chunk.objects.get(name=chunk_name)
		return chunk.content

shortcodes.add("chunk", ChunksAPI.shortcode)
