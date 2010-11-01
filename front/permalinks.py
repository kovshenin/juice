from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse

def get_patterns():
	return patterns('juice.front.views',
		(r'^$', 'index'),
		(r'^page/(?P<page>[\d]+)/$', 'index'),
		(r'^posts/(?P<post_slug>[-\w]+)/$', 'single'),
		(r'^category/(?P<category_slug>[-\w/]+)/$', 'category'),
		(r'^tag/(?P<tag_slug>[-\w]+)/$', 'tag'),
		(r'^(?P<slug>[-\w\/]+)/$', 'route'),

		# this is pseudo and is never reached as route is already defined
		# these are used for correct url resolving
		(r'^(?P<page_slug>[-\w]+)/$', 'page'),
	)

from juice.posts.models import Post
from juice.comments.models import Comment
from juice.taxonomy.models import Term
from juice.pages.models import Page

def make_permalink(object=None, prepend="", append=""):
	if object == None:
		return reverse('juice.front.views.index')
	
	if isinstance(object, Page):
		slug = object.slug

		if (object.is_root_node()):
			return reverse('juice.front.views.route', kwargs={'slug': slug})
		
		while (object.is_child_node()):
			parent = object.parent
			prepend = "%s/%s" % (parent.slug, prepend)
			object = parent
			
		return reverse('juice.front.views.route', kwargs={'slug': "%s%s" % (prepend, slug)})
		
	if isinstance(object, Post):
		slug = object.slug
		return reverse('juice.front.views.single', kwargs={'post_slug': slug})
	
	if isinstance(object, Term):
		slug = object.slug
		
		if object.taxonomy == "tag":
			return reverse('juice.front.views.tag', kwargs={'tag_slug': slug})
				
		if object.taxonomy == "category": # hierarchical
			if object.is_root_node():
				if object.taxonomy == "category":
					return reverse('juice.front.views.category', kwargs={'category_slug': slug})

			while (object.is_child_node()):
				parent = object.parent
				prepend = "%s/%s" % (parent.slug, prepend)
				object = parent
				
			return reverse('juice.front.views.category', kwargs={'category_slug': "%s%s" % (prepend, slug)})
