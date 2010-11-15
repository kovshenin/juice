from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.http import HttpRequest

def get_patterns():
	return patterns('juice.front.views',
		(r'^$', 'index'),
		(r'^page/(?P<page>[\d]+)/$', 'index'),
		(r'^posts/(?P<post_slug>[-\w]+)/$', 'single'),
		#(r'^category/(?P<category_slug>[-\w/]+)/$', 'category'),
		#(r'^tag/(?P<tag_slug>[-\w]+)/$', 'tag'),
		
		(r'^search/$', 'search'),		
		
		(r'^(?P<slug>[-\w\/]+)/$', 'route'),

		# This is pseudo and is never reached as route is already defined.
		# These are used for correct url resolving.
		(r'^(?P<page_slug>[-\w]+)/$', 'page'),
	)

from juice.posts.models import Post
#from juice.comments.models import Comment
#from juice.taxonomy.models import Term
from juice.pages.models import Page

def make_permalink(object=None, prepend="", append="", absolute=False, request=False):
	path = 'juice.front.views.index'
	args = ()
	kwargs = ()
	
	if isinstance(object, Page):
		path = 'juice.front.views.route'
		slug = object.slug

		if (not object.parent_page):
			kwargs = {'slug': slug}
		
		else:
			while (object.parent_page):
				parent = object.parent_page
				prepend = "%s/%s" % (parent.slug, prepend)
				object = parent

			kwargs = {'slug': "%s%s" % (prepend, slug)}

	elif isinstance(object, Post):
		slug = object.slug
		path = 'juice.front.views.single'
		kwargs = {'post_slug': slug}
	
	"""
	elif isinstance(object, Term):
		slug = object.slug
		
		if object.taxonomy == "tag":
			path = 'juice.front.views.tag'
			kwargs = {'tag_slug': slug}
				
		elif object.taxonomy == "category": # hierarchical
			path = 'juice.front.views.category'
			
			if object.is_root_node():
				kwargs = {'category_slug': slug}
			
			else:
				while (object.is_child_node()):
					parent = object.parent
					prepend = "%s/%s" % (parent.slug, prepend)
					object = parent
					
				kwargs = {'category_slug': "%s%s" % (prepend, slug)}
	"""
	
	permalink = reverse(path, args=args, kwargs=kwargs)
	
	if absolute:
		return request.build_absolute_uri(permalink)
	else:
		return permalink
