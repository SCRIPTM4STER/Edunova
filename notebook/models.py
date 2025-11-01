import uuid
from django.db import models
from accounts.models import User


class Notebook(models.Model):
    """
    Represents a collection or category of notes (like folders).
    Each user can have multiple notebooks.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notebooks')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['created_at']),
            models.Index(fields=['owner', 'created_at']),
        ]

    def __str__(self):
        return self.name


class Note(models.Model):
    """
    Represents individual notes inside a notebook.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='notes/', null=True, blank=True)
    is_public = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['notebook']),
            models.Index(fields=['is_public']),
            models.Index(fields=['is_deleted']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['owner', 'is_deleted']),
            models.Index(fields=['is_public', 'is_deleted']),
            models.Index(fields=['owner', 'is_deleted', 'updated_at']),
        ]

    def __str__(self):
        return f"{self.title} ({self.owner.username})"
