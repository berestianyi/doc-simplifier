import os
import re
from audioop import reverse

import PyPDF2
from django.http import Http404, FileResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView

from business_entities.models import BusinessEntitiesEnum, BusinessEntities
from business_entities.views import BusinessEntityMixin
from .forms import PDFUploadForm
from .models import Documents


class TextExtraction:
    fop_regex_dict = {
        'director_name': r'ФОП\s+(.+?)\s+Витяг з Єдиного державного реєстру юридичних осіб',
        'edrpou': r'Ідентифікаційний код:\s*(\d+)\s*Адреса:',
        'address': r'Адреса:\s*(.+?)\s*Статус:',
        'phone': r'Контактна інформація\s*Телефони:\s*(.+?)\s*(Email:.*|Дані про взяття на облік)',
        'email': r'Контактна інформація\s*Телефони:\s*.+?\s*Email:\s*(.+?)\s*Дані про взяття на облік',
    }

    tov_regex_dict = {
        'company_name': r'Повна назва: ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ\s\s*(.+?)\s*(Код:|Організаційно-правова форма:)',
        'edrpou': r'Код:\s*(.+?)\s*Реєстраційний номер:',
        'address': r'Адреса:\s*(.+?)\s*Статус:',
        'director_name': r'Керівник:\s*(.+?)\s*(Відомості про органи управління:|Засновник:|Представник:)',
        'phone': r'Контактна інформація(?:\s*Електронна пошта:.*?Телефон:| Телефон:.*?)\s*(.+?)\s*Дані про взяття на облік',
        'email': r'Контактна інформація\s*Електронна пошта:\s*(.+?)\s*Телефон:\s*(.+?)\s*Дані про взяття на облік',
    }

    def __init__(self, pdf_file):
        self.pdf_file = pdf_file

    def text_extraction(self):
        pdf_reader = PyPDF2.PdfReader(self.pdf_file)

        extracted_text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text

        extracted_text = extracted_text.replace('\n', ' ')
        extracted_text = re.sub(r'[‘’“”"«»]', '', extracted_text)

        return extracted_text

    def is_fop(self) -> bool:
        extracted_text = self.text_extraction()

        has_fop = bool(re.search(r'\bФОП\b', extracted_text))
        if has_fop:
            return True
        return False

    def extract_data(self) -> dict:
        extracted_text = self.text_extraction()

        is_fop = self.is_fop()

        if is_fop:
            regex_dict = self.fop_regex_dict
        else:
            regex_dict = self.tov_regex_dict

        extracted_data = {}
        for key, regex in regex_dict.items():
            match = re.search(regex, extracted_text, re.DOTALL)
            if match:
                extracted_data[key] = match.group(1).strip()
            else:
                extracted_data[key] = None
        return extracted_data


class PDFUploadView(FormView):
    template_name = 'documents/pdf_text_extraction.html'
    form_class = PDFUploadForm

    def form_valid(self, form):
        pdf_file = form.cleaned_data['pdf_file']
        text_extraction = TextExtraction(pdf_file)
        data = text_extraction.extract_data()
        print(data)

        business_entity_type = (
            BusinessEntitiesEnum.FOP if text_extraction.is_fop() else BusinessEntitiesEnum.TOV
        )

        business_entity = BusinessEntities.objects.create(
            business_entity=business_entity_type,
            edrpou=data.get('edrpou'),
            company_name=data.get('company_name'),
            director_name=data.get('director_name'),
            address=data.get('address'),
            email=data.get('email'),
            phone=data.get('phone'),
        )
        print(business_entity.id)
        return redirect('business_entities:business_entity_detail', business_entity_id=business_entity.id)





class DocumentsDetailListView(BusinessEntityMixin, ListView):
    model = Documents
    template_name = 'documents/detail_list.html'
    context_object_name = 'documents'
    paginate_by = 5

    def get_queryset(self):
        return Documents.objects.filter(
            contract__business_entities=self.business_entity
        )


class DocumentsDownloadView(View):
    def get(self, request, pk):
        document = Documents.objects.get(pk=pk)
        if not document.path:
            raise Http404("File not found.")
        file_path = document.path.path
        if os.path.exists(file_path):
            return FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=os.path.basename(file_path)
            )
        else:
            raise Http404("File not found.")
