from rest_framework import serializers
from .models import Notebook, Note


class NotebookSerializer(serializers.ModelSerializer):
    notes_count = serializers.IntegerField(source='notes.count', read_only=True)

    class Meta:
        model = Notebook
        fields = ['id', 'name', 'description', 'owner', 'created_at', 'updated_at', 'notes_count']
        read_only_fields = ['owner', 'created_at', 'updated_at', 'notes_count']


class NoteSerializer(serializers.ModelSerializer):
    notebook_name = serializers.CharField(source='notebook.name', read_only=True)

    class Meta:
        model = Note
        fields = [
            'id', 'title', 'content', 'image',
            'notebook', 'notebook_name', 'owner',
            'is_public', 'is_deleted',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']
