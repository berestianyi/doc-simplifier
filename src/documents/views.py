from django.shortcuts import redirect
from django.views import View
from django.views.generic import FormView

from business_entities.models import BusinessEntitiesEnum, BusinessEntities
from .forms import PDFUploadForm
from .mixins import DocumentMixin
from .models import Documents
from .services import TextExtraction


class PDFUploadView(FormView):
    template_name = 'documents/pdf_text_extraction.html'
    form_class = PDFUploadForm

    def form_valid(self, form):
        pdf_file = form.cleaned_data['pdf_file']
        text_extraction = TextExtraction(pdf_file)
        data = text_extraction.extract_data()

        business_entity_type = (
            BusinessEntitiesEnum.FOP if text_extraction.is_fop() else BusinessEntitiesEnum.TOV
        )

        address = TextExtraction.address_handler(data.get("address"))

        business_entity = BusinessEntities.objects.create(
            business_entity=business_entity_type,
            edrpou=data.get('edrpou'),
            company_name=data.get('company_name'),
            director_name=data.get('director_name'),
            address=address,
            email=data.get('email'),
            phone=data.get('phone'),
        )
        return redirect('business_entities:business_entity_detail', business_entity_id=business_entity.id)


class DocumentsDownloadView(DocumentMixin, View):
    def get(self, request, document_id):
        response = self.download_file(Documents, document_id)
        return response
