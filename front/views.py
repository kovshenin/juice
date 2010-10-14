from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from juice.news.models import Post
from juice.comments.models import Comment
from juice.taxonomy.models import Term
from juice.pages.models import Page

import juice.front.breadcrumbs

# homepage
def index(request):
	p = Post.objects.all().order_by('-published')[:10]
	pages = Page.objects.filter(parent__isnull=True).order_by('title')
	
	# set the permalinks
	for page in pages:
		page.permalink = reverse('juice.front.views.page', kwargs={'page_slug': page.slug})
		page.subpages = Page.objects.filter(parent__id=page.id).order_by('title')
		for subpage in page.subpages:
			subpage.permalink = reverse('juice.front.views.route', kwargs={'slug': "%s/%s" % (page.slug, subpage.slug)})
	
	return render_to_response('index.html', {'posts': p, 'pages': pages})
	
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
def page(request, page_slug):
	p = Page.objects.get(slug=page_slug)
	return render_to_response('page.html', {'page': p})

# This function routes all requests that didn't match any regex
def route(request, slug):
	slugs = slug.split('/')
	
	# remove double slashes
	while '' in slugs:
		slugs.remove('')

	parent = Page.objects.get(slug=slugs.pop(0), parent__id__isnull=True)
	
	for page_slug in slugs:
		p = Page.objects.get(slug=page_slug, parent__id=parent.id)
		parent = p
		
	# redirect to the page view
	return page(request, parent.slug)
