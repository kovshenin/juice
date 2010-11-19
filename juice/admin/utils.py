from django.conf.urls.defaults import *
from django.conf import settings

class AdminClass():
	registered_items = {}
	
	def __init__(self):
		self.initialized = True
		self.urlpatterns = patterns('juice.admin.views',
			(r'^$', 'dashboard'),
			(r'^list/(?P<object_slug>[-\w]+)/$', 'list'),
			(r'^edit/(?P<object_slug>[-\w]+)/(?P<object_id>.+)/$', 'edit'),
		)
		
	def autodiscover(self):
		for k in [k for k in settings.INSTALLED_APPS if k.startswith('juice')]:
			try:
				__import__(k + '.admin')
			except:
				pass
		
	def register(self, cls, options={}):
		self.registered_items[cls.__name__] = (cls, options)
		
admin = AdminClass()

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
