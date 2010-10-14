# News Module

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

if 'juice.taxonomy' in settings.INSTALLED_APPS:
	from juice.taxonomy.models import Term
	
# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=50)
	excerpt = models.TextField()
	content = models.TextField()
	published = models.DateTimeField('Date published')
	updated = models.DateTimeField('Date upated', auto_now=True, auto_now_add=True)
	author = models.ForeignKey(User)
	
	if 'juice.taxonomy' in settings.INSTALLED_APPS:
		terms = models.ManyToManyField(Term, blank=True)
	
	def __unicode__(self):
		return self.title
		
	class Meta:
		db_table = 'juice_news_post'
