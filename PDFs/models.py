import uuid
from django.db import models
from accounts.models import User
from notebook.models import Note
from django.core.validators import FileExtensionValidator

class PDF(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # File details
    file_name = models.CharField(max_length=255)
    file = models.FileField(
        upload_to="pdfs/files/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to="pdfs/covers/", blank=True, null=True)
    linked_note = models.ForeignKey(
        Note,
        on_delete=models.SET_NULL,  # Changed to SET_NULL for better data integrity if a Note is deleted.
        # If a Note is deleted, the PDF link is cleared, but the PDF record remains.
        # The original CASCADE is also valid if you want the PDF to be deleted when the Note is deleted.
        null=True,
        blank=True
    )

    # Ownership & access
    uploaded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="uploaded_pdfs"
    )
    is_public = models.BooleanField(default=False)


    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "PDF"
        verbose_name_plural = "PDFs"
        indexes = [
            models.Index(fields=['uploaded_by']),
            models.Index(fields=['is_public']),
            models.Index(fields=['created_at']),
            models.Index(fields=['linked_note']),
            models.Index(fields=['uploaded_by', 'is_public']),
            models.Index(fields=['uploaded_by', 'created_at']),
            models.Index(fields=['is_public', 'created_at']),
        ]

    def __str__(self) -> str:
        return self.file_name



