from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Page(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=50)
	content = models.TextField()
	
	published = models.DateTimeField('Date published')
	updated = models.DateTimeField('Date upated', auto_now=True, auto_now_add=True)
	
	author = models.ForeignKey(User)
	parent = models.ForeignKey('self', null=True, blank=True)
	
	def __unicode__(self):
		if self.parent:
			return "- %s" % self.title
		else:
			return self.title
		
	class Meta:
		db_table = 'juice_pages_page'
