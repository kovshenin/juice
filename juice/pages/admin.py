# Pages Admin
from juice.pages.models import Page
from juice.admin.utils import admin

page_admin = {
	'fields': ['title', 'content'],
	'editable_fields': ['title', 'slug', 'content'],
}

admin.register(Page, page_admin)
