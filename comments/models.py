# Comments Module

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

if 'juice.news' in settings.INSTALLED_APPS:
	from juice.news.models import Post

# Create your models here.
class Comment(models.Model):
	name = models.CharField(max_length=255)
	content = models.TextField()
	published = models.DateTimeField('Date published')
	updated = models.DateTimeField('Date upated', auto_now=True, auto_now_add=True)
	author = models.ForeignKey(User)
	
	if 'juice.news' in settings.INSTALLED_APPS:
		post = models.ForeignKey(Post)

	class Meta:
		db_table = 'juice_comments_comment'
