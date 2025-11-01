from rest_framework import serializers
from .models import PDF


MAX_PDF_MB = 10


class PDFSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PDF
        fields = [
            'id', 'file_name', 'file', 'title', 'description', 'cover_image',
            'linked_note', 'uploaded_by', 'is_public', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_file(self, value):
        if not value:
            return value
        # Size limit
        max_bytes = MAX_PDF_MB * 1024 * 1024
        if value.size and value.size > max_bytes:
            raise serializers.ValidationError(f"PDF size must be <= {MAX_PDF_MB} MB")
        # Content type hint (best-effort)
        content_type = getattr(value, 'content_type', None)
        if content_type and content_type not in ('application/pdf', 'application/x-pdf'):
            raise serializers.ValidationError("Uploaded file must be a PDF")
        return value

    def validate(self, attrs):
        linked_note = attrs.get('linked_note') or getattr(self.instance, 'linked_note', None)
        request = self.context.get('request')
        if linked_note and request and linked_note.owner != request.user:
            raise serializers.ValidationError({
                'linked_note': "You do not own the linked note."
            })
        return attrs

    def update(self, instance, validated_data):
        new_file = validated_data.get('file')
        if new_file and instance.file:
            # delete old file before replacing
            instance.file.delete(save=False)
        return super().update(instance, validated_data)

