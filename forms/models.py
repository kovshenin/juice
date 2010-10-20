from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.
class Form(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=50)

	published = models.DateTimeField('Date published')
	updated = models.DateTimeField('Date upated', auto_now=True, auto_now_add=True)
	
	author = models.ForeignKey(User)
	
	def __unicode__(self):
		return self.title
		
	class Meta:
		db_table = 'juice_forms_form'
		
	@staticmethod
	def get_form_by_id(form_id):
		try:
			form = Form.objects.get(id=form_id)
			return Form.get_form(form)
		except:
			pass
		
	@staticmethod
	def get_form_by_title(form_title):
		try:
			form = Form.objects.get(title=form_title)
			return Form.get_form(form)
		except:
			pass
		
	@staticmethod
	def get_form_by_slug(form_slug):
		try:
			form = Form.objects.get(slug=form_slug)
			return Form.get_form(form)
		except:
			pass
		
	@staticmethod
	def get_form(form_object):
		form = form_object
		form_fields = FormField.objects.filter(form__id=form.id)

		class NewForm(forms.Form):
			pass
			
		new_form = NewForm()
		
		for field in form_fields:
			if field.type == 'i':
				new_form.fields[field.name] = forms.CharField(max_length=255, required=field.required, label=field.caption)
			elif field.type == 't':
				new_form.fields[field.name] = forms.CharField(max_length=3000, required=field.required, widget=forms.Textarea, label=field.caption)
			elif field.type == 'c':
				new_form.fields[field.name] = forms.BooleanField(label=field.caption)
		
		return new_form

class FormField(models.Model):
	name = models.SlugField(max_length=50)
	caption = models.CharField(max_length=255)
	type = models.CharField(max_length=1, choices=(
		('i', 'Input'),
		('t', 'Textarea'),
		('s', 'Selectbox'),
		('c', 'Checkbox'),
		('r', 'Radio')
	))
	default_value = models.CharField(max_length=255, blank=True)
	required = models.BooleanField()

	form = models.ForeignKey(Form)

	class Meta:
		db_table = 'juice_forms_formfield'
