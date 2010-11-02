"""
	Usage: 
		1. {% menu_active request permalink %}

"""

from django import template

register = template.Library()

@register.tag
def menu_active(parser, token):
	tag_name, request, permalink = token.split_contents()
	return MenuActiveNode(request, permalink)
	
class MenuActiveNode(template.Node):
	def __init__(self, request, permalink):
		self.request = template.Variable(request)
		self.permalink = template.Variable(permalink)
	def render(self, context):
		request = self.request.resolve(context)
		permalink = self.permalink.resolve(context)
		
		if permalink == '':
			return ''
			
		if permalink == '/' and request.path != '/':
			return ''
		
		import re
		if re.search(permalink, request.path):
			return 'active'
		return ''
