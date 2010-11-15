# Comments Module
"""
# Django

from mptt.models import MPTTModel

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django import forms

if 'juice.news' in settings.INSTALLED_APPS:
	from juice.news.models import Post

# Create your models here.
class Comment(MPTTModel):
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	url = models.CharField(max_length=255)
	twitter = models.CharField(max_length=100)
	content = models.TextField()
	published = models.DateTimeField('Date published')
	updated = models.DateTimeField('Date upated', auto_now=True, auto_now_add=True)
	author = models.ForeignKey(User, blank=True, null=True)
	parent = models.ForeignKey('self', related_name='children', null=True, blank=True)

	object_id = models.PositiveIntegerField()
	content_type = models.ForeignKey(ContentType)
	content_object = generic.GenericForeignKey()
	
	def __unicode__(self):
		return '%s: "%s" on %s' % (self.name, self.content[:20], self.content_object.title)

	class Meta:
		db_table = 'juice_comments_comment'
		
	# use this method to preset additional properties
	def populate(self):
		import hashlib
		self.avatar = "http://www.gravatar.com/avatar/%s" % hashlib.md5(self.email.strip().lower()).hexdigest()
		
class CommentForm(forms.Form):
	name = forms.CharField(max_length=100, required=True)
	email = forms.EmailField(required=True)
	url = forms.URLField(max_length=255)
	twitter = forms.CharField(max_length=100)
	content = forms.CharField(required=True, widget=forms.Textarea)
	parent = forms.CharField(required=False, max_length=100)

"""

# Google AppEngine:

from google.appengine.ext import db

class Comment(db.Model):
	name = db.StringProperty(required=True)
	email = db.StringProperty(required=True)
	url = db.StringProperty()
	content = db.StringProperty(multiline=True)
	
	published = db.DateTimeProperty("Published", auto_now_add=True)
	updated = db.DateTimeProperty("Updated", auto_now_add=True, auto_now=True)
	
	parent_comment = db.SelfReferenceProperty("Parent", collection_name="comment_parent_reference")
	object_link = db.ReferenceProperty(collection_name="comment_object_link_reference")

	def populate(self):
		import hashlib
		self.avatar = "http://www.gravatar.com/avatar/%s" % hashlib.md5(self.email.strip().lower()).hexdigest()
		
		# @todo Check if this is fast and efficient enough, probably not
		# Should store the level value inside the database and count it
		# upon update, create or delete
		self.level = 0
		c = self.parent_comment
		
		while c:
			self.level += 1
			c = c.parent_comment
