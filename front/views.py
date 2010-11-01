import datetime
import os.path

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.template import RequestContext

from juice.posts.models import Post
from juice.comments.models import Comment, CommentForm
from juice.taxonomy.models import Term, TermRelation
from juice.pages.models import Page
from juice.forms.models import Form

from juice.front.permalinks import make_permalink

# homepage
def index(request, page=1):
	page = int(page)-1
	
	try:
		posts = Post.objects.all().order_by('-published')[page:10]
	except:
		raise Http404
	
	# is there anything left?
	if posts.count() == 0 & page > 0:
		raise Http404

	pages = Page.tree.all()
	tags = Term.objects.filter(taxonomy="tag")
	categories = Term.objects.filter(taxonomy="category")
	
	posts_ctype = ContentType.objects.get_for_model(Post)
	
	# set the permalinks
	for page in pages:
		page.permalink = make_permalink(page)
	for post in posts:
		post.permalink = make_permalink(post)
		post.comments_count = Comment.objects.filter(content_type__pk=posts_ctype.id, object_id=post.id).count()
	for tag in tags:
		tag.permalink = make_permalink(tag)
	for category in categories:
		category.permalink = make_permalink(category)
	
	ContactForm = Form.create_form_by_slug('contact-form')	
	if request.method == 'POST':
		contact_form = ContactForm(request.POST)
		if contact_form.is_valid():
			
			# Save the uploaded file
			cv = request.FILES['cv']
			dest = open(cv.name, 'wb+')
			for chunk in cv.chunks():
				dest.write(chunk)
			dest.close()
			
			contact_form = ContactForm()
	else:
		contact_form = ContactForm()	

	return render('home.html', {'posts': posts, 'pages': pages, 'tags': tags, 'categories': categories, 'contact_form': contact_form}, context_instance=RequestContext(request))
	
# single post view
def single(request, post_slug):
	p = Post.objects.get(slug=post_slug)
	ctype = ContentType.objects.get_for_model(Post)
	
	
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
		p = Page.objects.get(id=page_id)
	else:
		p = Page.objects.get(slug=page_slug)
	return render('page.html', {'page': p}, context_instance=RequestContext(request))

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
	main_menu = [
		{'title': 'Home', 'permalink': make_permalink()}
	]
	pages = Page.tree.filter(parent__id=None)
	# set the permalinks
	for page in pages:
		entry = {
			'title': page.title,
			'permalink': make_permalink(page),
		}
		main_menu.append(entry)
		
	main_menu.append({
		'name': 'contacts',
		'title': 'Contacts',
		'permalink': '',
	})
		
	context['global'] = {
		'title': 'Juice',
		'home': make_permalink(),
		'navigation': {
			'main': main_menu,
			'tray': [
				{'title': 'Home', 'permalink': make_permalink()},
				{'title': 'Products', 'permalink': ''},
				{'title': 'Services', 'permalink': ''},
				{'title': 'Feedback', 'permalink': ''},
				{'title': 'About', 'permalink': '/about/'},
			]
		},
	}
	
	return render_to_response(template_name, context, **kwargs)
