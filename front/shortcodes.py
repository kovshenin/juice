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
				parsed = re.sub(r'\[' + item + r'\]', result, parsed)
				
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
