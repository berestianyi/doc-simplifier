import os

from django.http import Http404, FileResponse
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from business_entities.models import BusinessEntities
from .models import Documents


class DocumentMixin:
    @cached_property
    def document(self):
        document_id = self.kwargs.get("document_id")
        if document_id is None:
            return None
        return get_object_or_404(Documents, pk=document_id)

    @staticmethod
    def business_entities_documents(business_entity: BusinessEntities):
        return Documents.objects.filter(
            contract__business_entities=business_entity
        ).order_by('-created_at')

    @staticmethod
    def download_file(model_with_path, file_id) -> FileResponse | Http404:
        file = model_with_path.objects.get(pk=file_id)
        if not file.path:
            raise Http404("File not found.")
        file_path = file.path.path
        if os.path.exists(file_path):
            return FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=os.path.basename(file_path)
            )
        else:
            raise Http404("File not found.")
