from juice.comments.models import Comment
from juice.admin.utils import admin

comment_admin = {
	'fields': ['name', 'content'],
	'editable_fields': ['name', 'email', 'url', 'content'],
}

admin.register(Comment, comment_admin)
