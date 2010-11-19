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
		if slugify(item) == object_slug:
			object_class = admin.registered_items[item][0]
			object_options = admin.registered_items[item][1]
			object_slug = slugify(item)
			
	objects = object_class.all()
	objects = objects.fetch(10)
	
	for object in objects:
		object.admin_fields = []
		for field in object_options['fields']:
			object.admin_fields.append({'caption': getattr(object, field), 'url': reverse('juice.admin.views.edit', args=[], kwargs={'object_slug': object_slug, 'object_id': object.key()})})

	return render('list.html', {'objects': objects, 'options': object_options})
	
def edit(request, object_slug, object_id):
	object_class = None
	
	for item in admin.registered_items:
		if slugify(item) == object_slug:
			object_class = admin.registered_items[item][0]
			object_options = admin.registered_items[item][1]
			object_slug = slugify(item)
			
	object = object_class.get(str(object_id))
	object.editable_fields = []
	
	for field in object_options['editable_fields']:
		object.editable_fields.append({'caption': field, 'current_value': getattr(object, field)})
	
	debug = {'id': str(object_id)}
	
	return render('edit.html', {'object': object, 'options': object_options, 'debug': debug})

def render(template_name, context={}, **kwargs):
	
	main_menu = []
	for item in admin.registered_items:
		entry = {'caption': item, 'url': reverse('juice.admin.views.list', args=[], kwargs={'object_slug': slugify(item)})}
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
