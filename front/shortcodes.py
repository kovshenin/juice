# The Juice Shortcodes API. To be transfered into the juice.core module.
# Needs a little bit more refactoring, but the general idea is to provide
# Pages, posts and other content types with the ability to use shortcodes.
# This is very similar to WordPress' technique. Examples of shortcodes could be:
#
# * [form slug="contact-form"] (Juice Forms API)
# * [chunk name="chunk-name"] (Juice Chunks API)
# 
# You can define your custom shortcodes using the shortcodes.add method,
# which does all the parsing for you and passes a dictionary with the attributes
# to the function you've provided. To apply the shortcodes to a string use
# the shortcodes.apply method, which could optionally accept a request argument
# to pass request data (such as POST data for forms) to your shortcode handler
import re
from juice.front.debug import debug

# Don't use this class directly, it is initiated at the end for general
# usage. The classes shortcodes property holds the currently active
# shortcodes. You can use the add and remove methods to control them.
class ShortcodeAPI():
	shortcodes = {}
	
	# Apply all the shortcodes to a string (content) and optionally
	# pass on the request object to shortcode handlers (for HTTP data
	# handling).
	def apply(self, content, request=None):
		pattern = re.compile(r'\[(.*?)\]')
		groups = pattern.findall(content)
		pieces = {}
		parsed = content
		
		# Loop through the found shortcode groups, parse their attributes
		# and call the handler functions accordingly.
		for item in groups:
			if ' ' in item:
				name, space, args = item.partition(' ')
				args = self.__parse_args__(args)
			else:
				name = item
				args = {}
				
			if request:
				args['request'] = request
			
			# Parse only shortcodes that were register with shortcodes.add
			if name in self.shortcodes:
				func = self.shortcodes[name]
				result = func(args)
				parsed = re.sub(r'\[' + re.escape(item) + r'\]', result, parsed)
			
		return parsed
	
	# Private method to parse shortcode attributes.
	def __parse_args__(self, value):
		ex = re.compile(r'[ ]*(\w+)=([^" ]+|"[^"]*")[ ]*(?: |$)')
		groups = ex.findall(value)
		kwargs = {}
	
		for group in groups:
			if group.__len__() == 2:
				item_key = group[0]
				item_value = group[1]
				
				if item_value.startswith('"'):
					if item_value.endswith('"'):
						item_value = item_value[1:]
						item_value = item_value[:item_value.__len__() - 1]
				
				kwargs[item_key] = item_value
		
		return kwargs
	
	# The two following methods can add and remove shortcodes, in other words
	# use them for shortcode registration and deregistration.
	def add(self, key, function):
		self.shortcodes[key] = function
		
	def remove(self, key):
		del self.shortcodes[key]

# This is the only instance of the ShortcodeAPI to be used outside this module.
shortcodes = ShortcodeAPI()

# Common shortcodes
class CommonShortcodes():

	@staticmethod
	def youtube(kwargs):
		url = kwargs.get("url").__str__()
		width = kwargs.get("width") or 640
		height = kwargs.get("height") or 384
		
		youtube_id = re.search(r'v=(.{11})', url).group(1)
		
		if url != None:
			return """
				<span class="youtube-video video" style="width: %(width)spx; height: %(height)spx;">
					<object width="%(width)s" height="%(height)s">
						<param name="movie" value="http://www.youtube.com/v/%(id)s?fs=1&amp;hl=en_US&amp;rel=0"></param>
						<param name="allowFullScreen" value="true"></param>
						<param name="allowscriptaccess" value="always"></param>
						<embed src="http://www.youtube.com/v/%(id)s?fs=1&amp;hl=en_US&amp;rel=0" 
							type="application/x-shockwave-flash" 
							allowscriptaccess="always" 
							allowfullscreen="true" 
							width="%(width)s" 
							height="%(height)s">
						</embed>
					</object>
				</span>
				""" % {'id': youtube_id, 'width': width, 'height': height}
				
	@staticmethod
	def snippet(kwargs):
		from django import template
		from django.template.loader import get_template

		snippet_name = kwargs.get("name") or False
		context = template.Context(kwargs)
		try:
			tp = get_template("snippets/%s" % snippet_name)
		except:
			return "Snippet %s not found!" % snippet_name

		return tp.render(context)


shortcodes.add('youtube', CommonShortcodes.youtube)
shortcodes.add('snippet', CommonShortcodes.snippet)
