from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.core.files.base import ContentFile

from .models import Notebook, Note
from .serializers import NotebookSerializer, NoteSerializer
from .permissions import IsOwnerOrReadOnly
from PDFs.models import PDF
from PDFs.serializers import PDFSerializer
from PDFs.utils.generator import generate_pdf_from_text

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


# Notebook Views
class NotebookListCreateView(generics.ListCreateAPIView):
    queryset = Notebook.objects.select_related('owner').all().order_by('-created_at')
    serializer_class = NotebookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



"""
This feature is not in use or unnecessary.
still kept it. maybe use later
"""
# class NotebookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Notebook.objects.select_related('owner').all().order_by('-created_at')
#     serializer_class = NotebookSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Notebook.objects.select_related('owner').order_by('-created_at')


class NoteListCreateView(generics.ListCreateAPIView):
    
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        # Users see their own notes or public notes
        return (
            Note.objects.select_related('owner', 'notebook')
            .filter(is_deleted=False)
            .filter(Q(owner=user) | Q(is_public=True))
            .order_by('-updated_at')
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Note.objects.select_related('owner', 'notebook').filter(is_deleted=False)


class GeneratePDFFromNoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            note = Note.objects.select_related('owner').get(pk=pk, is_deleted=False)
        except Note.DoesNotExist:
            return Response({'detail': 'Note not found.'}, status=status.HTTP_404_NOT_FOUND)

        if note.owner_id != request.user.id:
            return Response({'detail': 'Not permitted.'}, status=status.HTTP_403_FORBIDDEN)

        # Generate PDF bytes
        buffer = generate_pdf_from_text(note.title, note.content)
        pdf_bytes = buffer.getvalue()
        file_name = f"{note.title or 'note'}".replace(' ', '_') + ".pdf"

        pdf_instance = PDF(
            file_name=file_name,
            title=note.title,
            description=f"Generated from note {note.id}",
            linked_note=note,
            uploaded_by=request.user,
            is_public=False,
        )
        pdf_instance.file.save(file_name, ContentFile(pdf_bytes), save=True)

        data = PDFSerializer(pdf_instance, context={'request': request}).data
        return Response(data, status=status.HTTP_201_CREATED)
