# Taxonomy Module

from django.db import models

# Create your models here.
class Term(models.Model):
	taxonomy = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=50)
	description = models.TextField(blank=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		db_table = 'juice_taxonomy_term'
