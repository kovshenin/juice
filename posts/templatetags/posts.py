"""
	Usage: 
		{% posts_archive daily %}
		{% posts_archive monthly %}
		{% posts_archive yearly %}
		
	Outputs:
		<ul>
			<li>Entry (#)</li>
			...
		</ul>
"""
from django import template
from juice.posts.models import Post

register = template.Library()

@register.tag
def posts_archive(parser, token):
	tag_name, archive_type = token.split_contents()
	return PostsArchiveNode(archive_type)
	
class PostsArchiveNode(template.Node):
	def __init__(self, archive_type):
		self.archive_type = archive_type
	def render(self, context):
		archive = []
		archive_type = self.archive_type
		
		# depending on what kind of archive was requested
		if archive_type == "daily":
			dates = Post.objects.dates('published', 'day', 'DESC')
			for date in dates:
				count = Post.objects.filter(published__day=date.day, published__month=date.month, published__year=date.year).count()
				archive.append("<li>%s (%s)</li>" % (date.strftime("%d %B %Y"), count))
		elif archive_type == "monthly":
			dates = Post.objects.dates('published', 'month', 'DESC')
			for date in dates:
				count = Post.objects.filter(published__month=date.month, published__year=date.year).count()
				archive.append("<li>%s (%s)</li>" % (date.strftime("%B %Y"), count))
		elif archive_type == "yearly":
			dates = Post.objects.dates('published', 'year', 'DESC')
			for date in dates:
				count = Post.objects.filter(published__year=date.year).count()
				archive.append("<li>%s (%s)</li>" % (date.strftime("%Y"), count))
		
		# join the archive into an unordered list and return
		return "<ul>%s</ul>" % "".join(archive)
