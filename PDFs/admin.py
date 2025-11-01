from django.contrib import admin
from .models import PDF


@admin.register(PDF)
class PDFAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'title', 'uploaded_by', 'is_public', 'linked_note', 'created_at', 'updated_at')
    list_filter = ('is_public', 'created_at', 'updated_at')
    search_fields = ('file_name', 'title', 'description', 'uploaded_by__username', 'uploaded_by__email')
    list_per_page = 25
    list_max_show_all = 100
    list_editable = ('is_public',)
    list_display_links = ('id', 'file_name')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('uploaded_by', 'linked_note')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('file_name', 'title', 'description')
        }),
        ('Files', {
            'fields': ('file', 'cover_image')
        }),
        ('Relations', {
            'fields': ('uploaded_by', 'linked_note', 'is_public')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )