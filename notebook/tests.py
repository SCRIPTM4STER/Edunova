"""
Unit tests for notebook app.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Notebook, Note

User = get_user_model()


class NotebookModelTestCase(TestCase):
    """Test cases for Notebook model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_notebook_creation(self):
        """Test notebook is created correctly."""
        notebook = Notebook.objects.create(
            name='Test Notebook',
            description='Test Description',
            owner=self.user
        )
        self.assertEqual(notebook.name, 'Test Notebook')
        self.assertEqual(notebook.owner, self.user)
    
    def test_note_creation(self):
        """Test note is created correctly."""
        notebook = Notebook.objects.create(
            name='Test Notebook',
            owner=self.user
        )
        note = Note.objects.create(
            notebook=notebook,
            title='Test Note',
            content='Test Content',
            owner=self.user
        )
        self.assertEqual(note.title, 'Test Note')
        self.assertEqual(note.notebook, notebook)
        self.assertEqual(note.owner, self.user)


class NotebookAPITestCase(TestCase):
    """Test cases for Notebook API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.notebook = Notebook.objects.create(
            name='Test Notebook',
            owner=self.user
        )
        self.note = Note.objects.create(
            notebook=self.notebook,
            title='Test Note',
            content='Test Content',
            owner=self.user
        )
    
    def test_notebook_list_requires_authentication(self):
        """Test notebook list endpoint requires authentication."""
        url = reverse('notebook-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_notebook_list_authenticated(self):
        """Test notebook list endpoint with authentication."""
        self.client.force_authenticate(user=self.user)
        url = reverse('notebook-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_notebook_create_authenticated(self):
        """Test notebook creation with authentication."""
        self.client.force_authenticate(user=self.user)
        url = reverse('notebook-list-create')
        data = {'name': 'New Notebook', 'description': 'New Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Notebook.objects.filter(name='New Notebook').exists())
    
    def test_note_list_requires_authentication(self):
        """Test note list endpoint requires authentication."""
        url = reverse('note-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_note_list_authenticated(self):
        """Test note list endpoint with authentication."""
        self.client.force_authenticate(user=self.user)
        url = reverse('note-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_note_detail_authenticated(self):
        """Test note detail endpoint with authentication."""
        self.client.force_authenticate(user=self.user)
        url = reverse('note-detail', kwargs={'pk': self.note.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Note')
    
    def test_note_update_owner(self):
        """Test note update by owner."""
        self.client.force_authenticate(user=self.user)
        url = reverse('note-detail', kwargs={'pk': self.note.id})
        data = {'title': 'Updated Note', 'content': 'Updated Content'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Note')
