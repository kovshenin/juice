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
		#return reverse('juice.front.views.route', kwargs={'slug': "%s%s%s" % (prepend, object.slug, append)})
