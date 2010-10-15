from django.core.urlresolvers import reverse

from juice.news.models import Post
from juice.comments.models import Comment
from juice.taxonomy.models import Term
from juice.pages.models import Page

def make_permalink(object, prepend="", append=""):
	if isinstance(object, Page):
		slug = object.slug
		
		if (object.is_root_node()):
			return reverse('juice.front.views.route', kwargs={'slug': slug})
		
		while (object.is_child_node()):
			parent = object.parent
			prepend = "%s/%s" % (parent.slug, prepend)
			object = parent
			
		return reverse('juice.front.views.route', kwargs={'slug': "%s%s" % (prepend, slug)})
	
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
