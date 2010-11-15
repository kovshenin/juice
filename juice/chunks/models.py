"""
# Django

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
"""

# Google AppEngine

from google.appengine.ext import db
from juice.core.shortcodes import shortcodes

class Chunk(db.Model):
	name = db.StringProperty("Chunk Name", required=True)
	content = db.StringProperty("Content", multiline=True)
	
	published = db.DateTimeProperty("Published", auto_now_add=True)
	updated = db.DateTimeProperty("Updated", auto_now_add=True, auto_now=True)

class ChunksAPI():
	@staticmethod
	def shortcode(kwargs):
		chunk_name = kwargs.get("name").__str__()
		chunk = Chunk.all()
		chunk.filter('name =', chunk_name)
		chunk.get()
		
		if chunk.count() == 1:
			return chunk[0].content
		else:
			return chunk_name

shortcodes.add("chunk", ChunksAPI.shortcode)
