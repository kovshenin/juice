from mptt.models import MPTTModel

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from juice.front.permalinks import make_permalink

# Create your models here.
class Menu(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=50)

	published = models.DateTimeField('Date published', auto_now_add=True)
	updated = models.DateTimeField('Date upated', auto_now=True, auto_now_add=True)

	def populate(self):
		self.items = MenuItem.objects.filter(menu__id=self.id).order_by('order')
		for item in self.items:
			if item.content_object:
				item.permalink = make_permalink(item.content_object)
	
	def __unicode__(self):
		return self.title
	
	class Meta:
		db_table = 'juice_navigation_menu'

	pass
	
class MenuItem(MPTTModel):
	slug = models.SlugField(max_length=50, null=True, blank=True)
	caption = models.CharField(max_length=255, null=True, blank=True)
	permalink = models.CharField(max_length=255, null=True, blank=True)
	order = models.PositiveIntegerField(null=True, blank=True)
	
	# Menu Items can be hierarchical
	parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
	
	menu = models.ForeignKey(Menu)
	
	# In case we'd like to link to a dynamic object
	object_id = models.PositiveIntegerField(blank=True, null=True)
	content_type = models.ForeignKey(ContentType, blank=True, null=True)
	content_object = generic.GenericForeignKey()
	
	class Meta:
		db_table = 'juice_navigation_menuitem'

	def __unicode__(self):
		return self.caption

class MenuAPI():	
	@staticmethod
	def by_id(menu_id):
		try:
			menu = Menu.objects.get(id=menu_id)
			return MenuAPI.create_menu(menu)
		except:
			pass
			
	@staticmethod
	def by_slug(menu_slug):
		try:
			menu = Menu.objects.get(slug=menu_slug)
			return MenuAPI.create_menu(menu)
		except:
			pass
			
	@staticmethod
	def by_name(menu_name):
		try:
			menu = Menu.objects.get(name=menu_name)
			return MenuAPI.create_menu(menu)
		except:
			pass
			
	@staticmethod
	def create_menu(menu):
		menu.items = MenuItem.objects.filter(menu__id=menu.id).order_by('order')
		for item in menu.items:
			item.permalink = make_permalink(item)
		return menu
