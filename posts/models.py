# Posts Module

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=50)
	excerpt = models.TextField()
	content = models.TextField()
	published = models.DateTimeField('Date published')
	updated = models.DateTimeField('Date upated', auto_now=True, auto_now_add=True)
	author = models.ForeignKey(User)
	
	def __unicode__(self):
		return self.title
		
	class Meta:
		db_table = 'juice_posts_post'
