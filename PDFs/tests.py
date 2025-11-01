"""
Unit tests for PDFs app.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from .models import PDF
import uuid

User = get_user_model()


class PDFModelTestCase(TestCase):
    """Test cases for PDF model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_pdf_creation(self):
        """Test PDF is created correctly."""
        pdf = PDF.objects.create(
            file_name='test.pdf',
            title='Test PDF',
            uploaded_by=self.user,
            is_public=False
        )
        self.assertEqual(pdf.file_name, 'test.pdf')
        self.assertEqual(pdf.uploaded_by, self.user)
        self.assertFalse(pdf.is_public)
        self.assertIsNotNone(pdf.id)


class PDFAPITestCase(TestCase):
    """Test cases for PDF API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.pdf = PDF.objects.create(
            file_name='test.pdf',
            title='Test PDF',
            uploaded_by=self.user,
            is_public=False
        )
    
    def test_pdf_list_requires_authentication(self):
        """Test PDF list endpoint requires authentication."""
        url = reverse('pdf-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_pdf_list_authenticated(self):
        """Test PDF list endpoint with authentication."""
        self.client.force_authenticate(user=self.user)
        url = reverse('pdf-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data or [])
    
    def test_pdf_upload_requires_authentication(self):
        """Test PDF upload requires authentication."""
        url = reverse('pdf-upload')
        data = {'file_name': 'new.pdf', 'title': 'New PDF'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_pdf_detail_authenticated(self):
        """Test PDF detail endpoint with authentication."""
        self.client.force_authenticate(user=self.user)
        url = reverse('pdf-detail', kwargs={'pk': self.pdf.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file_name'], 'test.pdf')
    
    def test_pdf_delete_owner(self):
        """Test PDF deletion by owner."""
        self.client.force_authenticate(user=self.user)
        url = reverse('pdf-detail', kwargs={'pk': self.pdf.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PDF.objects.filter(id=self.pdf.id).exists())
    
    def test_pdf_public_access(self):
        """Test public PDF is accessible to authenticated users."""
        self.pdf.is_public = True
        self.pdf.save()
        
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=other_user)
        
        url = reverse('pdf-detail', kwargs={'pk': self.pdf.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
