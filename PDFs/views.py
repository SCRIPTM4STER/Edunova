from django.http import FileResponse, Http404
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from .models import PDF
from .serializers import PDFSerializer


class PDFPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class PDFUploadCreateView(generics.CreateAPIView):
    queryset = PDF.objects.all()
    serializer_class = PDFSerializer
    permission_classes = [permissions.IsAuthenticated]


class PDFListView(generics.ListAPIView):
    serializer_class = PDFSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PDFPagination

    def get_queryset(self):
        user = self.request.user
        return (
            PDF.objects.select_related('linked_note', 'uploaded_by')
            .filter(Q(uploaded_by=user) | Q(is_public=True))
            .order_by('-created_at')
        )


class PDFRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PDFSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Allow owners to access; public readable by anyone authenticated
        user = self.request.user
        return PDF.objects.select_related('linked_note', 'uploaded_by').filter(
            Q(uploaded_by=user) | Q(is_public=True)
        )

    def perform_destroy(self, instance):
        # Delete associated file from storage
        if instance.file:
            instance.file.delete(save=False)
        if instance.cover_image:
            instance.cover_image.delete(save=False)
        super().perform_destroy(instance)


class PDFDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            pdf = PDF.objects.get(pk=pk)
        except PDF.DoesNotExist:
            raise Http404

        if not (pdf.is_public or pdf.uploaded_by_id == request.user.id):
            return Response({'detail': 'Not found.'}, status=404)

        if not pdf.file:
            raise Http404

        response = FileResponse(pdf.file.open('rb'), content_type='application/pdf')
        disposition = f'attachment; filename="{pdf.file_name or (str(pdf.id) + ".pdf")}"'
        response['Content-Disposition'] = disposition
        return response


