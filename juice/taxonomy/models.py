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
		return "%s (%s)" % (self.name, self.taxonomy)

	class Meta:
		db_table = 'juice_taxonomy_term'
		
class TermRelation(models.Model):
	# relations
	term = models.ForeignKey(Term)
	object_id = models.PositiveIntegerField()
	content_type = models.ForeignKey(ContentType)
	content_object = generic.GenericForeignKey()
	
	def __unicode__(self):
		return "%s -- %s" % (self.term.name, self.content_object.title)
	
	class Meta:
		db_table = 'juice_taxonomy_relations'
		
	@staticmethod
	def get_objects_by_term_id(model=None, taxonomy=None, term_id=None, order_by='NULL'):
		data = {
			'objects': model._meta.db_table,
			'content_type': ContentType.objects.get_for_model(model).id,
			'relations': TermRelation._meta.db_table,
			'terms': Term._meta.db_table,
			'term_id': term_id,
			'order_by': ' ORDER BY %s ' % order_by
		}

		return model.objects.raw('SELECT %(objects)s.* FROM %(objects)s JOIN %(relations)s ON %(objects)s.id = %(relations)s.object_id AND %(relations)s.content_type_id = %(content_type)s JOIN %(terms)s ON %(relations)s.term_id = %(terms)s.id WHERE %(terms)s.id = %(term_id)s %(order_by)s' % data)

#mptt.register(Term)
