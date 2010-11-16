"""
# Django

from django.db import models

# Create your models here.
class OptionGroup(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=50)

	class Meta:
		db_table = 'juice_core_optiongroup'
		
	def __unicode__(self):
		return self.title

class Option(models.Model):
	group = models.ForeignKey(OptionGroup)
	name = models.SlugField(max_length=50)
	value = models.TextField(blank=True)

	published = models.DateTimeField('Date published', auto_now_add=True)
	updated = models.DateTimeField('Date upated', auto_now=True, auto_now_add=True)

	class Meta:
		db_table = 'juice_core_option'

	def __unicode__(self):
		return self.name
		
class OptionsAPI():
	@staticmethod
	def by_slug(group_slug):
		group = OptionGroup.objects.get(slug=group_slug)
		options = Option.objects.filter(group__id=group.id)
		return options

"""

# Google AppEngine

from google.appengine.ext import db

class OptionGroup(db.Model):
	title = db.StringProperty(required=True)
	slug = db.StringProperty(required=True)
	
class Option(db.Model):
	group = db.ReferenceProperty(OptionGroup)
	name = db.StringProperty("Name", required=True)
	value = db.StringProperty("Value", multiline=True)
	
	published = db.DateTimeProperty("Date Published", auto_now_add=True)
	updated = db.DateTimeProperty("Date Updated", auto_now_add=True, auto_now=True)
	
class OptionsAPI():
	@staticmethod
	def by_slug(group_slug):
		group = OptionGroup.all()
		group.filter('slug =', group_slug)
		group = group.get() or None
		
		if group:
			options = Option.all()
			options.filter('group =', group.key())
			options = options.fetch(1000)
		
			return options
		
		else:
			return []
