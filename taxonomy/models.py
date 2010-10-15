# Taxonomy Module

from django.db import models
from mptt.models import MPTTModel

# Create your models here.
class Term(MPTTModel):
	taxonomy = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=50)
	description = models.TextField(blank=True)
	parent = models.ForeignKey('self', related_name='children', null=True, blank=True)

	def __unicode__(self):
		return self.name

	class Meta:
		db_table = 'juice_taxonomy_term'

#mptt.register(Term)
