from django import template
from juice.taxonomy.models import Term
from juice.news.models import Post

register = template.Library()

@register.tag
def taxonomy_list(parser, token):
	tag_name, terms = token.split_contents()
	return TaxonomyNode(terms)
	
class TaxonomyNode(template.Node):
	def __init__(self, terms):
		self.terms = template.Variable(terms)
	def render(self, context):
		terms = self.terms.resolve(context)
		links = []

		for term in terms:
			links.append('<a href="%s">%s</a>' % (term.permalink, term.name))

		return ", ".join(links)
