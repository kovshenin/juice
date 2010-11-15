# Juice Front Middleware. This module contains a set of classes that could be
# used as middleware to Django.

import tidy
import django.conf

# The Tidy middleware prettifies HTML markup, can remove broken validation
# and a bunch of other cool stuff. This certainly gives a slight impact on
# performance, but if your caching is right, you can afford it.
#
# Debug mode is also available. Via debug mode you can view Tidy error reports
# on your old HTML by sending a 'notidy' GET variable to any URL. If DEBUG
# is switched on in Django settings, you'll find the errors listed at the end
# of your HTML output as comments.
#
# For a full list of Tidy options and sweeties, visit:
# http://tidy.sourceforge.net/docs/quickref.html
class Tidy(object):
	def __init__(self):
		self.tidy_options = dict(output_xhtml=True,
								add_xml_decl=True,
								doctype='strict',
								indent='yes',
								indent_spaces='4',
								tidy_mark=False,
								hide_comments=True,
								wrap=100,
								force_output=True)

	# This method is called by the middleware mechanism in Django
	def process_response(self, request, response):
		if response['Content-Type'].split(';', 1)[0] == 'text/html':
			content = response.content
			content = tidy.parseString(content, **self.tidy_options)
			
			# Notidy in DEBUG mode will attempt to Tidy the response, but doesn't
			# replace the original one so that error lines and numbers in the
			# errors list are correct. Use this for convenient templates validation.
			if 'notidy' not in request.GET or not django.conf.settings.DEBUG:
				response.content = content.__str__()
			
			# List the errors if DEBUG is on at the end of the response text
			if content.errors and django.conf.settings.DEBUG:
				response.content += "<!-- Validation Errors:\n"
				for error in content.errors:
					response.content += "%s\n" % error.__str__()
				response.content += "-->"
				
		return response
