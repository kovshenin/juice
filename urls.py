from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Example:
	# (r'^juice/', include('juice.foo.urls')),
	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
	(r'^$', 'juice.front.views.index'),
	(r'^posts/(?P<post_slug>[-\w]+)/$', 'juice.front.views.single'),
	(r'^category/(?P<category_slug>[-\w]+)/$', 'juice.front.views.category'),
	(r'^tag/(?P<tag_slug>[-\w]+)/$', 'juice.front.views.tag'),
	(r'^(?P<slug>[-\w\/]+)/$', 'juice.front.views.route'),
	(r'^(?P<page_slug>[-\w]+)/$', 'juice.front.views.page'),
)
