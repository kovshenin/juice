from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from juice.news.models import Post
from juice.comments.models import Comment
from juice.taxonomy.models import Term
from juice.pages.models import Page

from juice.front.permalinks import make_permalink

# homepage
def index(request):
	posts = Post.objects.all().order_by('-published')[:10]
	pages = Page.tree.all()
	tags = Term.objects.filter(taxonomy="tag")
	categories = Term.objects.filter(taxonomy="category")
	
	# set the permalinks
	for page in pages:
		page.permalink = make_permalink(page)
	for post in posts:
		post.permalink = make_permalink(post)
	for tag in tags:
		tag.permalink = make_permalink(tag)
	for category in categories:
		category.permalink = make_permalink(category)
	
	return render_to_response('index.html', {'posts': posts, 'pages': pages, 'tags': tags, 'categories': categories})
	
# single post view
def single(request, post_slug):
	p = Post.objects.get(slug=post_slug)
	p.tags = p.terms.filter(taxonomy='tag')
	p.categories = p.terms.filter(taxonomy='category')
	
	# set the permalinks
	for c in p.categories:
		c.permalink = reverse('juice.front.views.category', kwargs={'category_slug': c.slug})
	for t in p.tags:
		t.permalink = reverse('juice.front.views.tag', kwargs={'tag_slug': t.slug})
		
	p.comments = Comment.objects.filter(post=p.id).order_by('-published')
	return render_to_response('news-single.html', {'post': p})
	
# view by category
def category(request, category_slug):
	c = Term.objects.get(slug=category_slug, taxonomy='category')
	p = Post.objects.filter(terms__id=c.id)
	return render_to_response('news-list.html', {'posts': p, 'category': c})

# view by tag
def tag(request, tag_slug):
	t = Term.objects.get(slug=tag_slug, taxonomy='tag')
	p = Post.objects.filter(terms__id=t.id)
	return render_to_response('news-list.html', {'posts': p, 'tag': t})

# single page view
def page(request, page_slug, page_id=False):
	if page_id:
		p = Page.objects.get(id=page_id)
	else:
		p = Page.objects.get(slug=page_slug)
	return render_to_response('page.html', {'page': p})

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
	
	
	# otherwise check if the parent/child is okay	
	parent = Page.objects.get(slug=slugs.pop(0), parent__id__isnull=True)
	
	for page_slug in slugs:
		p = Page.objects.get(slug=page_slug, parent__id=parent.id)
		parent = p
		
	last_child = parent
		
	# redirect to the page view if everything's fine otherwise an exception is thrown
	return page(request, last_child.slug, page_id=last_child.id)
