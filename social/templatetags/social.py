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

from juice.core.models import OptionsAPI

register = template.Library()

@register.tag
def social_share(parser, token):
	tag_name, permalink = token.split_contents()
	return SocialShareNode(permalink)
	
class SocialShareNode(template.Node):
	def __init__(self, permalink):
		self.permalink = template.Variable(permalink)
	def render(self, context):
		permalink = self.permalink.resolve(context)
		options = OptionsAPI.by_slug("juice-social-share")
		widgets = []
		for option in options:
			widgets.append(option.value % {'permalink': permalink})
			
		return ' '.join(widgets)
