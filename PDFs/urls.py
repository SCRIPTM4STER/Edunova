from django.urls import path
from .views import (
    PDFUploadCreateView,
    PDFListView,
    PDFRetrieveUpdateDestroyView,
    PDFDownloadView,
)

urlpatterns = [
    path('upload/', PDFUploadCreateView.as_view(), name='pdf-upload'),
    path('', PDFListView.as_view(), name='pdf-list'),
    path('<uuid:pk>/', PDFRetrieveUpdateDestroyView.as_view(), name='pdf-detail'),
    path('<uuid:pk>/download/', PDFDownloadView.as_view(), name='pdf-download'),
]