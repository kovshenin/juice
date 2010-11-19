# Posts Admin

from juice.posts.models import Post
from juice.admin.utils import admin

post_admin = {
	'fields': ['title', 'slug', 'excerpt'],
	'editable_fields': ['title', 'slug', 'content'],
}

admin.register(Post, post_admin)
