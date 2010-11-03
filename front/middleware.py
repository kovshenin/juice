import tidy
import django.conf

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

	def process_response(self, request, response):
		if response['Content-Type'].split(';', 1)[0] == 'text/html':
			content = response.content
			content = tidy.parseString(content, **self.tidy_options)
			
			if 'notidy' not in request.GET or not django.conf.settings.DEBUG:
				response.content = content.__str__()
			
			if content.errors and django.conf.settings.DEBUG:
				response.content += "<!-- Validation Errors:\n"
				for error in content.errors:
					response.content += "%s\n" % error.__str__()
				response.content += "-->"
				
		return response
