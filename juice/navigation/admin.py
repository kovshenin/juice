from django.contrib import admin
from juice.navigation.models import Menu, MenuItem

class MenuItemInline(admin.TabularInline):
	model = MenuItem
	extra = 3

class MenuAdmin(admin.ModelAdmin):
	inlines = [MenuItemInline]
	
admin.site.register(Menu, MenuAdmin)
