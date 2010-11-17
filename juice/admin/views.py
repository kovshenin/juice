# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse

from juice.admin.utils import admin

def dashboard(request):
	return render('dashboard.html')
	
def list(request, object_slug):
	object_class = None
	for item in admin.registered_items:
		if slugify(item.__name__) == object_slug:
			object_class = item
			
	objects = object_class.all()
	objects = objects.fetch(1000)
			
	return render('list.html', {'objects': objects})

def render(template_name, context={}, **kwargs):
	
	main_menu = []
	for item in admin.registered_items:
		entry = {'caption': item.__name__, 'url': reverse('juice.admin.views.list', args=[], kwargs={'object_slug': slugify(item.__name__)})}
		main_menu.append(entry)
		
	navigation = {
		'main': main_menu
	}
	
	# Form the global context here, these variables are passed to each and every template
	# rendered via juice.front.views.render(). You can add additional variables which can
	# be used in your base template or children.
	context['global'] = {
		'title': 'Juice Administration',
		'navigation': navigation,
	}
	
	# Render the final response based on the JUICE_THEME Django setting. Note that this structure
	# is mandatory for Juice templates to work correctly. If you're looking to change URL styles
	# to access dynamic and static data, use the permalinks.py file and urls.py respectively.
	return render_to_response(template_name, context, **kwargs)

# Slugify
import re
import unicodedata

def slugify(value):
	_slugify_strip_re = re.compile(r'[^\w\s-]')
	_slugify_hyphenate_re = re.compile(r'[-\s]+')

	if not isinstance(value, unicode):
		value = unicode(value)
	value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
	value = unicode(_slugify_strip_re.sub('', value).strip().lower())
	return _slugify_hyphenate_re.sub('-', value)
