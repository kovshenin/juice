from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.
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
		
	@staticmethod
	def create_form_by_id(form_id):
		try:
			form = Form.objects.get(id=form_id)
			return Form.create_form(form)
		except:
			pass
		
	@staticmethod
	def create_form_by_title(form_title):
		try:
			form = Form.objects.get(title=form_title)
			return Form.create_form(form)
		except:
			pass
		
	@staticmethod
	def create_form_by_slug(form_slug):
		try:
			form = Form.objects.get(slug=form_slug)
			return Form.create_form(form)
		except:
			pass

	@staticmethod
	def create_form(form_object):
		form = form_object
		form_fields = FormField.objects.filter(form__id=form.id)

		class _FutureForm(forms.Form):
			title = form.title
			def __init__(self, *args, **kwargs):
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

		return _FutureForm

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
	))
	attributes = models.TextField(blank=True)
	default_value = models.TextField(blank=True)
	required = models.BooleanField()

	form = models.ForeignKey(Form)

	class Meta:
		db_table = 'juice_forms_formfield'
