from django.urls import path
from .views import (
    NotebookListCreateView,
    NoteListCreateView,
    NoteRetrieveUpdateDestroyView,
    GeneratePDFFromNoteView,
    # NotebookRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('notebooks/', NotebookListCreateView.as_view(), name='notebook-list-create'),
    # path('notebooks/<uuid:pk>/', NotebookRetrieveUpdateDestroyView.as_view(), name='notebook-list-create'),
    path('notes/', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<uuid:pk>/', NoteRetrieveUpdateDestroyView.as_view(), name='note-detail'),
    path('notes/<uuid:pk>/generate-pdf/', GeneratePDFFromNoteView.as_view(), name='note-generate-pdf'),
]
