from django import template

from juice.core.models import OptionsAPI
from juice.core.debug import debug

register = template.Library()

@register.tag
def social(parser, token):
	try:
		tag_name, option_name, object = token.split_contents()
		return SocialNodeObject(option_name, object)
	except ValueError:
		tag_name, option_name = token.split_contents()
		return SocialNodePlain(option_name)	
	
class SocialNodeObject(template.Node):
	def __init__(self, option_name, object):
		self.option_name = template.Variable(option_name)
		self.object = template.Variable(object)
	def render(self, context):
		object = self.object.resolve(context)
		option_name = self.option_name.resolve(context)
		
		# Let's loop though all the object attributes and form a formatting
		# dict by tag name with their values. We'll use this for replacements.
		context = {}
		for tag in dir(object):
			if not tag.startswith('_'):
				try:
					context[tag] = getattr(object, tag)
				except AttributeError:
					pass
					
		cx = template.Context(context)
			
		# Get the social options
		options = OptionsAPI.by_slug(option_name.__str__())
		widgets = []
		for option in options:
			tp = template.Template(option.value.strip())
			widgets.append(tp.render(cx))
			
		return ''.join(widgets)

class SocialNodePlain(template.Node):
	def __init__(self, option_name):
		self.option_name = template.Variable(option_name)
	def render(self, context):
		option_name = self.option_name.resolve(context)
		
		options = OptionsAPI.by_slug(option_name.__str__())
		widgets = []
		for option in options:
			widgets.append(option.value.strip())
			
		return ''.join(widgets)
