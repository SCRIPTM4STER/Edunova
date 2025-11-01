from django.contrib import admin
from .models import Notebook, Note


@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'notes_count', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description', 'owner__username', 'owner__email')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('owner',)
    date_hierarchy = 'created_at'
    
    def notes_count(self, obj):
        return obj.notes.count()
    notes_count.short_description = 'Notes Count'


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'notebook', 'is_public', 'is_deleted', 'created_at', 'updated_at')
    list_filter = ('is_public', 'is_deleted', 'created_at', 'updated_at', 'notebook')
    search_fields = ('title', 'content', 'owner__username', 'owner__email', 'notebook__name')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('owner', 'notebook')
    date_hierarchy = 'created_at'
    list_editable = ('is_public', 'is_deleted')
