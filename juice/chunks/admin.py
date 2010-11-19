from juice.chunks.models import Chunk
from juice.admin.utils import admin

chunk_admin = {
	'fields': ['name', 'content'],
	'editable_fields': ['name', 'content'],
}
admin.register(Chunk, chunk_admin)
