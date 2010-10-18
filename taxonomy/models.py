# Taxonomy Module

from django.db import models
from mptt.models import MPTTModel

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

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
		
class TermRelation(models.Model):
	# relations
	term = models.ForeignKey(Term)
	object_id = models.PositiveIntegerField()
	content_type = models.ForeignKey(ContentType)
	content_object = generic.GenericForeignKey()
	
	class Meta:
		db_table = 'juice_taxonomy_relations'

#mptt.register(Term)
