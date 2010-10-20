from django.contrib import admin
from juice.forms.models import Form, FormField

class FormFieldInline(admin.TabularInline):
	model = FormField
	extra = 3

class FormAdmin(admin.ModelAdmin):
	inlines = [FormFieldInline]
	
admin.site.register(Form, FormAdmin) 
