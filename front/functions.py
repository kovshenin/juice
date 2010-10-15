from django.core.urlresolvers import reverse

from juice.news.models import Post
from juice.comments.models import Comment
from juice.taxonomy.models import Term
from juice.pages.models import Page

def make_permalink(object, prepend="", append=""):
	if isinstance(object, Page):
		return reverse('juice.front.views.route', kwargs={'slug': "%s%s%s" % (prepend, object.slug, append)})
