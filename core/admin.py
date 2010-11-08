from django.contrib import admin
from juice.core.models import Option, OptionGroup

class OptionInline(admin.TabularInline):
	model = Option
	extra = 3

class OptionAdmin(admin.ModelAdmin):
	inlines = [OptionInline]
	
admin.site.register(OptionGroup, OptionAdmin) 
