# Juice Forms 0.0.1 including the Juice Forms API
# by Konstantin Kovshenin
# 
# The following module is an addition to the Juice framework built upon
# the Django web framework. Uses Django users and django forms as seen
# from the import statements.

# Compatible with the Juice shortcodes API, allows usage of the [form]
# shortcode where applicable.

from django.db import models
from django.contrib.auth.models import User
from django import forms

from juice.front.shortcodes import shortcodes
from juice.front.debug import debug

# The standard Form model which is extended via FormField objects
# This is the one that appears in the admin panel.
class Form(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=50)

	published = models.DateTimeField('Date published', auto_now_add=True)
	updated = models.DateTimeField('Date upated', auto_now=True, auto_now_add=True)
	
	author = models.ForeignKey(User)
	
	def __unicode__(self):
		return self.title
		
	class Meta:
		db_table = 'juice_forms_form'

# Form fields are very similar to django form fields, but this is designed
# to handle input from the admin panel, where users can select the field
# type and several other attributes. Has a foreign key on Form.
class FormField(models.Model):
	name = models.SlugField(max_length=50)
	caption = models.CharField(max_length=255)
	type = models.CharField(max_length=1, choices=(
		('i', 'Input'),
		('e', 'E-mail'),
		('t', 'Textarea'),
		('s', 'Selectbox'),
		('c', 'Checkbox'),
		('r', 'Radio'),
		('f', 'File Attachment'),
		('x', 'Submit'),
	))
	attributes = models.TextField(blank=True)
	default_value = models.TextField(blank=True)
	required = models.BooleanField()

	form = models.ForeignKey(Form)

	class Meta:
		db_table = 'juice_forms_formfield'

# The Juice Forms API. This is a class consisting mostly of static methods
# which produce form objects based on the form fields and forms, sort of a
# Factory. The Action pool is essential to the Forms API which will tell
# what type of actions we'd like the form to produce on submit (email, etc).
class FormsAPI():
	
	# The following create methods are used to lookup forms in the database
	# parse their attributes and fields, and give out a valid form class
	# which could be used anywhere.
	
	@staticmethod
	def create_form_by_id(form_id):
		try:
			form = Form.objects.get(id=form_id)
			return FormsAPI.create_form(form)
		except:
			pass
		
	@staticmethod
	def create_form_by_title(form_title):
		try:
			form = Form.objects.get(title=form_title)
			return FormsAPI.create_form(form)
		except:
			pass
		
	@staticmethod
	def create_form_by_slug(form_slug):
		try:
			form = Form.objects.get(slug=form_slug)
			return FormsAPI.create_form(form)
		except:
			pass

	# This method does the actual form generation, so if you're looking
	# to add more possible fields, this is a place to look at how they're
	# formed, returns a valid form class.
	@staticmethod
	def create_form(form_object):
		form = form_object
		form_fields = FormField.objects.filter(form__id=form.id)

		# This is our future class which we will return later
		class _FutureForm(forms.Form):
			title = form.title
			slug = form.slug
			extra = []
			
			# We init the parent form and then add more fields to the form
			# depending on what we've been given in the form_fields attribute.
			def __init__(self, *args, **kwargs):
				self.extra = [] # This will hold extra fields which are not specified by the Django forms module.
				super(_FutureForm, self).__init__(*args, **kwargs)
				for field in form_fields:
					if field.type == 'i': # Input
						self.fields[field.name] = forms.CharField(max_length=255, required=field.required, label=field.caption)
					elif field.type == 'e': # E-mail
						self.fields[field.name] = forms.EmailField(max_length=255, required=field.required, label=field.caption)
					elif field.type == 't': # Textarea
						self.fields[field.name] = forms.CharField(max_length=3000, required=field.required, widget=forms.Textarea, label=field.caption)
					elif field.type == 'c': # Checkbox
						self.fields[field.name] = forms.BooleanField(label=field.caption, required=field.required)
					elif field.type == 's': # Selectbox
						field_choices = []
						for attr in field.attributes.split("\n"):
							field_choices.append(attr.split(":"))
						self.fields[field.name] = forms.ChoiceField(choices=field_choices)
					elif field.type == 'r': # Radio
						field_choices = []
						for attr in field.attributes.split("\n"):
							field_choices.append(attr.split(":"))
						self.fields[field.name] = forms.ChoiceField(choices=field_choices, required=field.required, widget=forms.RadioSelect, label=field.caption)
					elif field.type == 'f': # File
						self.fields[field.name] = forms.FileField(label=field.caption, required=field.required)
					elif field.type == 'x': # Submit button
						self.extra.append('<input type="submit" name="%s" value="%s" />' % (field.name, field.caption))
			
			# In case we'd like to print this form.
			def __unicode__(self):
				return self.title
			
			# Rewrite the default django forms as_p statement to include
			# a div container around the form, the form tag, the form contents
			# (which are taken from the parent's as_p output and the form
			# extras (submit button, etc).
			def as_p(self):
				result = """<div class="juice-form form-%(form_slug)s">
								<form method="POST">
									%(form_contents)s
									%(form_extra)s
								</form>
							</div>""" % {'form_slug': self.slug, 'form_contents': super(_FutureForm, self).as_p(), 'form_extra': ' '.join(self.extra)}
				return result
		
		# Once the future form is constructed, return it.
		return _FutureForm

	# Use this static method to process any incoming form data. This
	# is under a lot of thinking at the mo, but we'll tie up a pool
	# of available actions that will be carried out on form submission.
	# Meanwhile we simply write to the debug log.
	@staticmethod
	def process_form(form_class, request):
		CustomForm = form_class
		if request != None and request.method == 'POST':
			form = CustomForm(request.POST)
			if form.is_valid():
				# @todo Action here
				debug("Submitted: %s" % form)
				form = CustomForm()
		else:
			form = CustomForm()
		
		return form
		
	# Do not call this static method directly unless you're 100% sure
	# about what you're doing. This tends to use the Juice Shortcode API
	# to display forms in posts, pages and other content types that Juice
	# provides. For more information check out the juice.front.shortcodes
	# package.
	@staticmethod
	def shortcode(kwargs):
		id = kwargs.get("id")
		slug = kwargs.get("slug").__str__()
		title = kwargs.get("title").__str__()
		request = kwargs.get("request")
		
		# In priority order, find the parameter that we should use
		# to identify the form.
		
		if id != None:
			NewForm = FormsAPI.create_form_by_id(int(id))

		elif slug != None:
			NewForm = FormsAPI.create_form_by_slug(slug)
			
		elif title != None:
			NewForm = FormsAPI.create_form_by_title(title)
		
		# Fire a form processing passing on the request. If the request
		# hasn't submitted any form data, process_form will return a new
		# form of the passed class
		form = FormsAPI.process_form(NewForm, request)
		
		# If everything's fine output the form using our re-written
		# as_p method, otherwise return some debug data.
		if form != None:
			return form.as_p()
		else:
			return kwargs.__unicode__()

# Using the Shortcodes API (juice.front.shortcodes) add a new shortcode
# called form. The general usage is: 

# * [form id="1"]
# * [form slug="contact-form"]
# * [form name="My Form Name"]
shortcodes.add("form", FormsAPI.shortcode)

# Use this to accept non-static methods in the Forms API
# Reserved for the action pool which will be worked out at a later
# stage.
api = FormsAPI()
