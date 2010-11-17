from django.conf.urls.defaults import *
from django.conf import settings

from juice.front.permalinks import get_patterns
from juice.admin.utils import admin

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
	# Example:
	# (r'^juice/', include('juice.foo.urls')),
	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	(r'^admin/', include(admin.urlpatterns)),
	#(r'^admin/', include(admin.site.urls)),
)

# get additional url patterms from juice.front
urlpatterns += get_patterns()
