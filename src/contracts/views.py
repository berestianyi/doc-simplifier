import os

import pymorphy3

from django.db.models import Q
from django.forms import model_to_dict
from django.http import Http404, FileResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, View, CreateView, UpdateView

from docx import Document
from python_docx_replace import docx_replace

from business_entities.models import BusinessEntities
from config import settings
from vehicles.models import Vehicles
from .forms import ContractTimeRangeForm, TemplatesForm
from .models import Templates, Contracts

morph = pymorphy3.MorphAnalyzer(lang='uk')


class ReplacementManager:
    MONTH_NAMES_UA = {
        1: "січня",
        2: "лютого",
        3: "березня",
        4: "квітня",
        5: "травня",
        6: "червня",
        7: "липня",
        8: "серпня",
        9: "вересня",
        10: "жовтня",
        11: "листопада",
        12: "грудня",
    }

    def __init__(
            self, start_date, expire_date, business_entity, vehicles, bank
    ):
        self.start_date = start_date
        self.expire_date = expire_date
        self.bank = bank
        self.business_entity = business_entity
        self.vehicles = vehicles

    @classmethod
    def upper_or_empty_str(cls, text: str) -> str:
        if text:
            return text.upper()

        return ""

    @classmethod
    def title_or_empty_str(cls, text: str) -> str:
        if text:
            return text.title()

        return ""

    @classmethod
    def to_genitive(cls, full_name: str) -> str:
        tokens = full_name.split()
        result_tokens = []

        for token in tokens:
            parsed = morph.parse(token)
            best_parse = parsed[0]
            gent_form = best_parse.inflect({'gent'})
            if gent_form:
                result_tokens.append(gent_form.word)
            else:
                result_tokens.append(token)
        return " ".join(result_tokens)

    @classmethod
    def guess_gender_pronoun(cls, name: str) -> str:
        if name:
            parsed = morph.parse(name)[0]
            gender = parsed.tag.gender
            if gender == 'masc':
                return 'який'
            elif gender == 'femn':
                return 'яка'
            else:
                return 'що'

        return ""

    def name_crusher(self, full_name: str) -> dict:
        tokens = full_name.split()
        last_name = tokens[0] if len(tokens) > 0 else ""
        first_name = tokens[1] if len(tokens) > 1 else ""
        middle_name = tokens[2] if len(tokens) > 2 else ""

        return {
            "last_name": self.title_or_empty_str(last_name),
            "upper_last_name": self.upper_or_empty_str(last_name),
            "first_name": self.title_or_empty_str(first_name),
            "upper_first_name": self.upper_or_empty_str(first_name),
            "middle_name": self.title_or_empty_str(middle_name),
            "upper_middle_name": self.upper_or_empty_str(middle_name),
            "upper_director_name": self.upper_or_empty_str(full_name),
            "gender_pronoun": self.guess_gender_pronoun(first_name),
            "genitive_director_name": self.to_genitive(full_name),
            "upper_genitive_director_name": self.upper_or_empty_str(self.to_genitive(full_name)),
        }

    def upper_company_name(self, company_name: str) -> dict:
        return {
            "upper_company_name": self.upper_or_empty_str(company_name),
        }

    def date_dict_generator(self) -> dict:
        return {
            "start_day": f"{self.start_date.day:02d}",
            "start_month": self.MONTH_NAMES_UA[self.start_date.month],
            "start_year": str(self.start_date.year),
            "expire_day": f"{self.expire_date.day:02d}",
            "expire_month": self.MONTH_NAMES_UA[self.expire_date.month],
            "expire_year": str(self.expire_date.year)
        }

    def document_number_generator(self) -> dict:
        return {
            "document_number": f"{self.start_date.day:02d}/{self.start_date.month}",
        }

    def replacements_generator(self) -> dict:
        bank_dict = model_to_dict(self.bank, fields=[
            "name",
            "mfo",
        ])

        business_entity_dict = model_to_dict(self.business_entity, fields=[
            "business_entity",
            "edrpou",
            "company_name",
            "director_name",
            "address",
            "email",
            "phone",
            "iban",
        ])

        name_crasher_dict = self.name_crusher(business_entity_dict.get("director_name"))
        upper_company_name_dict = self.upper_company_name(business_entity_dict.get("company_name"))
        date_dict = self.date_dict_generator()
        document_number_dict = self.document_number_generator()

        merged_dict = {
            **bank_dict,
            **business_entity_dict,
            **name_crasher_dict,
            **upper_company_name_dict,
            **date_dict,
            **document_number_dict
        }
        return merged_dict

    def cars_info_generator(self) -> list:
        vehicles_list = self.vehicles.values_list(
            "brand", "model", "number", "year"
        )
        return list(vehicles_list)


class WordDocManager:
    def __init__(self, template_path):
        self.doc = Document(template_path)

    def replace_placeholders(self, replacement: dict):
        doc = self.doc
        docx_replace(
            doc=doc,
            **replacement,
        )

    @classmethod
    def find_table_index_by_header(cls, doc) -> int:
        search_words = ["Марка, модель", "Реєстраційний номер"]
        for table_index, table in enumerate(doc.tables):
            table_text = " ".join(cell.text for row in table.rows for cell in row.cells)
            if all(word in table_text for word in search_words):
                return table_index
        return -1

    def add_car_info_to_table(self, cars_info: list):
        doc = self.doc

        table_index = self.find_table_index_by_header(doc)

        table = doc.tables[table_index]

        for count, car in enumerate(cars_info, start=1):
            row_cells = table.add_row().cells
            row_cells[0].paragraphs[0].add_run(str(count)).bold = True
            row_cells[1].paragraphs[0].add_run(str(car[0]) + ", " + str(car[1])).bold = True
            row_cells[2].paragraphs[0].add_run(str(car[2])).bold = True
            row_cells[3].paragraphs[0].add_run(str(car[3])).bold = True

    @staticmethod
    def create_output_filename(template: Templates, business_entity: BusinessEntities, contract_index) -> str:
        if business_entity.company_name:
            return f"{template.name}_{business_entity.company_name}_{contract_index}.docx"

        return f"{template.name}_{business_entity.director_name}_{contract_index}.docx"

    def save_word_file(self, filename: str = "output.docx") -> str:
        doc = self.doc
        output_path = os.path.join(settings.MEDIA_ROOT, "documents", filename)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        doc.save(output_path)
        return output_path


def create_contract_templates_search_form(request, business_entity_id):
    business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
    templates = Templates.objects.all()

    return render(
        request,
        'contract_templates/partials/templates_search_form.html',
        {
            'templates': templates,
            'business_entity': business_entity,
        }
    )


def search_contract_templates(request, business_entity_id):
    business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
    query = request.GET.get('q', '')

    templates = (
        Templates.objects
        .filter(
            Q(name__icontains=query)
        )
    )

    return render(
        request,
        'contract_templates/partials/templates_search_list.html',
        {
            'templates': templates,
            'query': query,
            'business_entity': business_entity,
        }
    )


def create_document_detail_list(request, business_entity_id):
    business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
    contracts = Contracts.objects.filter(business_entities_id=business_entity_id)

    return render(
        request,
        'contracts/detail.html',
        {
            'business_entity': business_entity,
            'contracts': contracts,
        }
    )


def create_contract(request, business_entity_id, template_id):
    business_entity = get_object_or_404(BusinessEntities, pk=business_entity_id)
    template = get_object_or_404(Templates, pk=template_id)
    bank = business_entity.bank
    if request.method == "POST":
        time_range_form = ContractTimeRangeForm(request.POST)
        if time_range_form.is_valid():
            vehicles_with_entities = (
                Vehicles.objects
                .filter(vehiclelicences__business_entities=business_entity)
                .distinct()
            )
            start_date = time_range_form.cleaned_data["start_date"]
            expire_date = time_range_form.cleaned_data["end_date"]

            contract = Contracts.objects.create(
                business_entities=business_entity,
                template=template,
                start_date=start_date,
                end_date=expire_date,
            )

            replacement_manager = ReplacementManager(
                start_date=start_date,
                expire_date=expire_date,
                business_entity=business_entity,
                bank=bank,
                vehicles=vehicles_with_entities,
            )
            word_manager = WordDocManager(template_path=template.path.path)

            replacement_dict = replacement_manager.replacements_generator()
            cars_dict = replacement_manager.cars_info_generator()

            word_manager.replace_placeholders(replacement_dict)
            word_manager.add_car_info_to_table(cars_dict)

            filename = word_manager.create_output_filename(template, business_entity, contract.id)
            output = word_manager.save_word_file(filename=filename)

            contract.name = filename
            contract.path = output
            contract.save()

            contracts = Contracts.objects.filter(business_entities_id=business_entity_id)

            return render(request, "contracts/detail.html", {
                "time_range_form": time_range_form,
                'business_entity': business_entity,
                'template': template,
                'contracts': contracts,
            })
    else:
        time_range_form = ContractTimeRangeForm()

    return render(request, "contracts/partials/create_form.html", {
        'time_range_form': time_range_form,
        'business_entity': business_entity,
        'template': template,
    })


class ContractTemplatesListView(ListView):
    model = Templates
    template_name = 'contract_templates/list.html'
    context_object_name = 'templates'
    paginate_by = 10


def create_template(request):
    if request.method == 'POST':
        form = TemplatesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('contracts:templates')
    else:
        form = TemplatesForm()

    context = {
        'template_form': form,
    }
    return render(request, 'contract_templates/create.html', context)


def update_template(request, template_id):
    template = get_object_or_404(Templates, pk=template_id)
    if request.method == 'POST':
        form = TemplatesForm(request.POST, request.FILES, instance=template)
        if form.is_valid():
            form.save()
            return redirect('contracts:templates')

    else:
        form = TemplatesForm(instance=template)

    context = {
        'template_form': form,
        'template': template,
    }
    return render(request, 'contract_templates/update.html', context)


def redirect_to_templates_list(request):
    response = HttpResponse("")
    redirect_url = reverse("contracts:templates")
    response["HX-Redirect"] = redirect_url
    return response


class TemplatesDownloadView(View):
    def get(self, request, pk):
        template = Templates.objects.get(pk=pk)
        if not template.path:
            raise Http404("File not found.")
        file_path = template.path.path
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
        else:
            raise Http404("File not found.")
