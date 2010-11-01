"""
	Usage: 
		1. {% chunk "name" %}
		
		Where "name" is the name of the chunk to return
		
	Outputs:
		1. The chunk contents or empty string if the chunk was not found
"""

from django import template
from juice.chunks.models import Chunk

register = template.Library()

@register.tag
def chunk(parser, token):
	tag_name, chunk_name = token.split_contents()
	return ChunkNode(chunk_name)
	
class ChunkNode(template.Node):
	def __init__(self, chunk_name):
		self.chunk_name = template.Variable(chunk_name)
	def render(self, context):
		# Read the chunk and try to fetch it from the database.
		chunk_name = self.chunk_name.resolve(context)
		chunk = Chunk.objects.get(name=chunk_name)
		return chunk.content
