from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from business_entities.forms import FOPCreateForm, TOVCreateForm
from .forms import PDFUploadForm
from .mixins import DocumentMixin
from .models import Documents
from .services.core import DocumentService


class PDFUploadView(View):
    template_name = 'documents/pdf_text_extraction.html'
    form_class = PDFUploadForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if not form.is_valid():
            return JsonResponse({
                'success': False,
            }, status=400)

        pdf_file = form.files.get('pdf_file')
        service = DocumentService(pdf_file)
        data = service.extract_data()
        if service.is_fop(data.get('edrpou')):
            form_class = FOPCreateForm
            template = 'business_entities/partials/forms/_fop_create.html'
        else:
            form_class = TOVCreateForm
            template = 'business_entities/partials/forms/_tov_create.html'

        create_form = form_class(initial={
            'edrpou': data.get('edrpou'),
            'company_name': data.get('company_name'),
            'director_name': data.get('director_name'),
            'address': data.get('address'),
            'phone': data.get('phone'),
            'email': data.get('email'),
        })

        return render(
            request,
            template,
            {
                'business_entity_form': create_form
            }
        )


class DocumentsDownloadView(DocumentMixin, View):
    def get(self, request, document_id):
        response = self.download_file(Documents, document_id)
        return response
