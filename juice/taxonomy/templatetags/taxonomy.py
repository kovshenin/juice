"""
	Usage: 
		1. {% taxonomy_list terms %}
		2. {% taxonomy_cloud terms %}
		
		Where "terms" is a list of juice.taxonomy.models.Term
		
	Outputs:
		1. A list of comma-separated terms with links to them
		2. A cloud of terms (useful for tag clouds)
"""

from django import template
from juice.taxonomy.models import Term

register = template.Library()

@register.tag
def taxonomy_list(parser, token):
	tag_name, terms = token.split_contents()
	return TaxonomyListNode(terms)
	
@register.tag
def taxonomy_cloud(parser, token):
	tag_name, terms = token.split_contents()
	return TaxonomyCloudNode(terms)
	
class TaxonomyCloudNode(template.Node):
	def __init__(self, terms):
		self.terms = template.Variable(terms)
	def render(self, context):
		terms = self.terms.resolve(context)
		cloud = []
		counts = []
		
		# count the terms usage @todo permalinks
		for term in terms:
			term.count = TermRelation.objects.filter(term__id=term.id).count()
			counts.append(term.count)
			
		maximum = max(counts)
		minimum = min(counts)
		count = terms.count()
		
		min_font_size = 15
		max_font_size = 20
		spread = maximum - minimum
		if spread == 0:
			spread = 1
		
		for term in terms:
			font_size = min_font_size + (term.count - minimum) * (max_font_size - min_font_size) / spread
			cloud.append('<a style="font-size: %spx" title="%s has been used %s times">%s</a>' % (font_size, term.name, term.count, term.name))
		
		return ", ".join(cloud)
	
class TaxonomyListNode(template.Node):
	def __init__(self, terms):
		self.terms = template.Variable(terms)
	def render(self, context):
		terms = self.terms.resolve(context)
		links = []

		for term in terms:
			links.append('<a href="%s">%s</a>' % (term.permalink, term.name))

		return ", ".join(links)
