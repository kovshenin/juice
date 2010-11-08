from datetime import datetime
import os.path

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.paginator import Paginator
from django.conf import settings

from juice.posts.models import Post
from juice.comments.models import Comment, CommentForm
from juice.taxonomy.models import Term, TermRelation
from juice.pages.models import Page
from juice.navigation.models import Menu
from juice.front.shortcodes import shortcodes

import juice.forms.models

from juice.front.permalinks import make_permalink

# homepage
def index(request, page=1):
	posts_list = Post.objects.filter(published__lte=datetime.now()).order_by('-published')
	paginator = Paginator(posts_list, 5)
	
	try:
		p = paginator.page(page)
	except (EmptyPage, InvalidPage):
		p = paginator.page(paginator.num_pages)
		
	posts = p.object_list

	p.next_link = reverse('juice.front.views.index', kwargs={'page': p.next_page_number()})
	p.previous_link = reverse('juice.front.views.index', kwargs={'page': p.previous_page_number()})
	
	posts_ctype = ContentType.objects.get_for_model(Post)

	for post in posts:
		post.permalink = make_permalink(post)
		post.comments_count = Comment.objects.filter(content_type__pk=posts_ctype.id, object_id=post.id).count()
		post.content = shortcodes.apply(post.content, request)

	return render('home.html', {'posts': posts, 'paginator': p}, context_instance=RequestContext(request))
	
# single post view
def single(request, post_slug):
	p = Post.objects.get(slug=post_slug, published__lte=datetime.now())
	ctype = ContentType.objects.get_for_model(Post)	
	
	# Apply the shortcodes to the post content
	p.content = shortcodes.apply(p.content, request)
	
	# read the relations with posts and terms
	rel_tags = TermRelation.objects.filter(content_type__pk=ctype.id, object_id=p.id, term__taxonomy='tag')
	rel_categories = TermRelation.objects.filter(content_type__pk=ctype.id, object_id=p.id, term__taxonomy='category')
	
	p.tags = []
	p.categories = []

	for tag in rel_tags:
		p.tags.append(tag.term)
	for category in rel_categories:
		p.categories.append(category.term)
	
	# form processing
	if request.method == 'POST':
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			comment = Comment(
				name=comment_form.cleaned_data['name'],
				email=comment_form.cleaned_data['email'],
				url=comment_form.cleaned_data['url'],
				twitter=comment_form.cleaned_data['twitter'],
				content=comment_form.cleaned_data['content'],
				author=User.objects.get(id=1),
				published=datetime.datetime.now(),
				content_object=p
			)
			
			try:
				parent_comment = Comment.objects.get(id=int(comment_form.cleaned_data['parent']))
				comment.parent = parent_comment
			except:
				pass
			
			comment.save()
			comment_form = CommentForm()
	else:
		comment_form = CommentForm()
	
	# set the permalinks
	p.permalink = make_permalink(p)
	for c in p.categories:
		c.permalink = make_permalink(c)
	for t in p.tags:
		t.permalink = make_permalink(t)
		
	# comments
	p.comments = Comment.tree.filter(content_type__pk=ctype.id, object_id=p.id)
	
	for c in p.comments:
		c.permalink = make_permalink(c)
		c.populate()
	
	p.comments_count = p.comments.count()
	
	return render('post.html', {'post': p, 'comment_form': comment_form}, context_instance=RequestContext(request))
	
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

# single page view
def page(request, page_slug, page_id=False):
	if page_id:
		page = Page.objects.get(id=page_id)
	else:
		page = Page.objects.get(slug=page_slug)

	page.content = shortcodes.apply(page.content, request)
	page.permalink = make_permalink(page)
	
	return render('page.html', {'page': page}, context_instance=RequestContext(request))

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
		parent = Page.objects.get(slug=slugs.pop(0), parent__id__isnull=True)

		for page_slug in slugs:
			p = Page.objects.get(slug=page_slug, parent__id=parent.id)
			parent = p

		last_child = parent
			
		# redirect to the page view if everything's fine otherwise an exception is thrown
		return page(request, last_child.slug, page_id=last_child.id)
	
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
	available_menus = Menu.objects.all()
	for menu in available_menus:
		navigation[menu.slug] = []
		menu.populate() # Populates the menu permalinks from linked objects
		
		for item in menu.items:
			navigation[menu.slug].append({
				'caption': item.caption,
				'permalink': item.permalink,
			})

	# Form the global context here, these variables are passed to each and every template
	# rendered via juice.front.views.render(). You can add additional variables which can
	# be used in your base template or children.
	context['global'] = {
		'title': 'Juice',
		'home': make_permalink(),
		'navigation': navigation
	}
	
	# Render the final response based on the JUICE_THEME Django setting. Note that this structure
	# is mandatory for Juice templates to work correctly. If you're looking to change URL styles
	# to access dynamic and static data, use the permalinks.py file and urls.py respectively.
	return render_to_response("%s/%s" % (settings.JUICE_THEME, template_name), context, **kwargs)
