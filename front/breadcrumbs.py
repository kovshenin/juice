from juice.pages.models import Page
from django.db.models.signals import post_init

def breadcrumbs(sender, **kwargs):
	#page = sender
	#page.permalink = 
	#while True:
	#p = Page.objects.get(id=1)
	pass

post_init.connect(breadcrumbs, sender=Page, weak=False)
