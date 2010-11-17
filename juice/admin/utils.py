from django.conf.urls.defaults import *
from django.conf import settings

class AdminClass():
	registered_items = []
	
	def __init__(self):
		self.initialized = True
		self.urlpatterns = patterns('juice.admin.views',
			(r'^$', 'dashboard'),
			(r'^list/(?P<object_slug>[-\w]+)/$', 'list'),
		)
		
	def autodiscover(self):
		for k in [k for k in settings.INSTALLED_APPS if k.startswith('juice')]:
			try:
				__import__(k + '.admin')
			except:
				pass
		
	def register(self, cls):
		self.registered_items.append(cls)
		
admin = AdminClass()
