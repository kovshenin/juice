from datetime import datetime
import os.path

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
#from django.contrib.contenttypes.models import ContentType
#from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.paginator import Paginator
from django.conf import settings

from juice.core.shortcodes import shortcodes
from juice.posts.models import Post
#from juice.comments.models import Comment
from juice.taxonomy.models import Term
from juice.pages.models import Page
from juice.navigation.models import Menu
#from juice.front.debug import debug

#from juice.forms.models import FormsAPI
from juice.front.permalinks import make_permalink

# homepage
def index(request, page=1):
	posts_list = Post.all()
	posts_list.order('-published')
	#posts_list.filter(published__lte=datetime.now()).order_by('-published')
	paginator = Paginator(posts_list, 5)
	
	try:
		p = paginator.page(page)
	except (EmptyPage, InvalidPage):
		p = paginator.page(paginator.num_pages)
		
	posts = p.object_list

	p.next_link = reverse('juice.front.views.index', kwargs={'page': p.next_page_number()})
	p.previous_link = reverse('juice.front.views.index', kwargs={'page': p.previous_page_number()})
	
	#posts_ctype = ContentType.objects.get_for_model(Post)

	for post in posts:
		post.permalink = make_permalink(post)
		post.permalink_abs = make_permalink(post, absolute=True, request=request)
		#post.comments_count = Comment.objects.filter(content_type__pk=posts_ctype.id, object_id=post.id).count()
		post.content = shortcodes.apply(post.content, request)

	return render('home.html', {'posts': posts, 'paginator': p})
	
def search(request):
	query = request.GET.get('q')
	page = request.GET.get('page') or 1
	
	from django.db.models import Q
	import operator
	
	words = query.split(' ')
	qs = []
	
	for word in words:
		qs.append(Q(title__icontains=word))
		qs.append(Q(content__icontains=word))
	
	posts = Post.objects.filter(reduce(operator.or_, qs))
	paginator = Paginator(posts, 5)
	
	try:
		p = paginator.page(page)
	except (EmptyPage, InvalidPage):
		p = paginator.page(paginator.num_pages)
		
	results = p.object_list
	
	for result in results:
		result.permalink = make_permalink(result, absolute=True, request=request)
	
	meta = {'query': query}
	
	return render('search.html', {'results': results, 'meta': meta, 'paginator': p}, context_instance=RequestContext(request))

# single post view
def single(request, post_slug):
	#p = Post.objects.get(slug=post_slug, published__lte=datetime.now())
	#p.ctype = ContentType.objects.get_for_model(Post)
	
	# Apply the shortcodes to the post content
	#p.content = shortcodes.apply(p.content, request)
	
	# read the relations with posts and terms
	#rel_tags = TermRelation.objects.filter(content_type__pk=p.ctype.id, object_id=p.id, term__taxonomy='tag')
	#rel_categories = TermRelation.objects.filter(content_type__pk=p.ctype.id, object_id=p.id, term__taxonomy='category')
	
	#p.tags = []
	#p.categories = []

	#for tag in rel_tags:
	#	p.tags.append(tag.term)
	#for category in rel_categories:
	#	p.categories.append(category.term)
	
	# set the permalinks
	#p.permalink = make_permalink(p)
	#for c in p.categories:
	#	c.permalink = make_permalink(c)
	#for t in p.tags:
	#	t.permalink = make_permalink(t)
		
	# comments
	#p.comments = Comment.tree.filter(content_type__pk=p.ctype.id, object_id=p.id)
	
	#for c in p.comments:
	#	c.permalink = make_permalink(c)
	#	c.populate()
	
	#p.comments_count = p.comments.count()
	
	#CommentForm = FormsAPI.by_slug('comment-form')
	#comment_form, feedback = FormsAPI.process_form(CommentForm, request, content_object=p, feedback=True)
	
	#for entry in feedback:
	#	action, arg = entry
	#	if action == "redirect_to":
	#		return HttpResponseRedirect(arg)
	
	p = Post.all()
	p.filter('slug =', post_slug)
	p.get()
	
	if p.count() == 1:
		p = p[0]
		p.content = shortcodes.apply(p.content, request)
		
		p.tags = []
		p.categories = []
		
		categories = Term.all()
		categories.filter('taxonomy =', 'category')
		categories.filter('relations =', p.key())
		categories = categories.fetch(1000)
		
		tags = Term.all()
		tags.filter('taxonomy =', 'tag')
		tags.filter('relations = ', p.key())
		tags = tags.fetch(1000)
		
		for c in categories:
			c.permalink=make_permalink(c)
			p.categories.append(c)
			
		for t in tags:
			t.permalink=make_permalink(t)
			p.tags.append(t)
		
		return render('post.html', {'post': p})
	else:
		raise Http404

"""
# view posts by category
def category(request, category_slug, page=1):
	page = int(page)-1
	
	posts = []
	ctype = ContentType.objects.get_for_model(Post)
	category = Term.objects.get(slug=category_slug, taxonomy='category')

	posts = TermRelation.get_objects_by_term_id(model=Post, taxonomy='category', term_id=category.id, order_by='published DESC')
	return render_to_response('news-list.html', {'posts': posts, 'category': category}, context_instance=RequestContext(request))

# view by tag
def tag(request, tag_slug, page=1):
	page = int(page)-1
	
	posts = []
	ctype = ContentType.objects.get_for_model(Post)
	tag = Term.objects.get(slug=tag_slug, taxonomy='tag')
	
	posts = TermRelation.get_objects_by_term_id(model=Post, taxonomy='tag', term_id=tag.id, order_by='published DESC')
	return render_to_response('news-list.html', {'posts': posts, 'tag': tag}, context_instance=RequestContext(request))
"""

# single page view
def page(request, page_slug, page=False):
	if not page:
		page = Page.all()
		page.filter('slug =', page_slug)

	page.content = shortcodes.apply(page.content, request)
	page.permalink = make_permalink(page)
	page.permalink_abs = make_permalink(page, absolute=True, request=request)
	
	return render('page.html', {'page': page})

# This function routes all requests that didn't match any regex
def route(request, slug):
	slugs = slug.split('/')

	# remove double slashes
	i = 0
	while '' in slugs:
		i += 1
		slugs.remove('')

	# redirect to the clean URL
	if i > 0:
		return HttpResponseRedirect('/%s/' % '/'.join(slugs))
	
	try:

		# otherwise check if the parent/child is okay	
		parent = Page.all()
		parent.filter('slug =', slugs.pop(0))
		parent.filter('parent_page =', None)
		parent = parent.get()
		last_child = parent
		
		for page_slug in slugs:
			child = Page.all()
			child.filter('slug =', page_slug)
			child.filter('parent_page =', parent.key())
			last_child = child.get()
			parent = last_child
			
		# redirect to the page view if everything's fine otherwise an exception is thrown
		return page(request, last_child.slug, page=last_child)
	
	except:
		raise Http404

# The following function does render_to_response along with the global
# variables used by the base template (base.html). This reduces
# redundant code.
def render(template_name, context={}, **kwargs):
	
	# Generate the navigation options based on what's in the navigation tables.
	# Loop through the items and add them to the navigation dict, which is passed
	# with the context in the global variable. This can be used in your templates
	# by accessing global.navigation.menuslug (no spaces, dots or dashes in the slugs).
	navigation = {}
	available_menus = Menu.all()
	available_menus = available_menus.fetch(1000)
	for menu in available_menus:
		navigation[menu.slug] = []
		menu.populate() # Populates the menu permalinks from linked objects
		
		for item in menu.items:
			navigation[menu.slug].append({
				'caption': item.caption,
				'permalink': item.permalink,
			})
	
	# Temp menu for AppEngine
	#navigation['topright'] = [
	#	{'caption': 'About', 'permalink': '/about/'},
	#	{'caption': 'Sitemap', 'permalink': '/sitemap/'},
	#	{'caption': 'Feedback', 'permalink': '/feedback/'}
	#]

	# Form the global context here, these variables are passed to each and every template
	# rendered via juice.front.views.render(). You can add additional variables which can
	# be used in your base template or children.
	context['global'] = {
		'title': 'Juice',
		'home': make_permalink(),
		'navigation': navigation,
		#'tags': Term.objects.filter(taxonomy='category')
	}
	
	# Render the final response based on the JUICE_THEME Django setting. Note that this structure
	# is mandatory for Juice templates to work correctly. If you're looking to change URL styles
	# to access dynamic and static data, use the permalinks.py file and urls.py respectively.
	return render_to_response(template_name, context, **kwargs)

"""
# Comment form action
def comment_form_action(form_object, **kwargs):
	obj = kwargs.get("content_object") or False
	
	if not obj:
		return

	comment_form = form_object
	comment = Comment(
		name=comment_form.cleaned_data['name'],
		email=comment_form.cleaned_data['email'],
		url=comment_form.cleaned_data['url'],
		twitter=comment_form.cleaned_data['twitter'],
		content=comment_form.cleaned_data['content'],
		author=User.objects.get(id=1),
		published=datetime.now(),
		content_object=obj,
	)
	
	try:
		parent_comment = Comment.objects.get(id=int(comment_form.cleaned_data['parent']))
		comment.parent = parent_comment
	except:
		pass
	
	comment.save()
	return ('redirect_to', "%s#div-comment-%s" % (obj.permalink, comment.id))

FormsAPI.add_action('comment-form', comment_form_action)
"""
