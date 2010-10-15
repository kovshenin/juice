from django import template
from juice.taxonomy.models import Term
from juice.news.models import Post

register = template.Library()

@register.tag
def taxonomy_tags(parser, token):
	tag_name, terms = token.split_contents()
	return TaxonomyNode(terms, "tag")
	
@register.tag
def taxonomy_categories(parser, token):
	tag_name, terms = token.split_contents()
	return TaxonomyNode(terms, "category")

class TaxonomyNode(template.Node):
	def __init__(self, terms, taxonomy="tag"):
		self.terms = template.Variable(terms)
		self.taxonomy = taxonomy
	def render(self, context):
		terms = self.terms.resolve(context).filter(taxonomy=self.taxonomy)
		links = []

		for term in terms.all():
			links.append('<a href="%s">%s</a>' % (term.permalink, term.name))
			
		return ", ".join(links)
