from django import forms
from datetime import date, timedelta

from src.contracts.models import Contracts, Templates


class RoyalForm(forms.ModelForm):
    tax_type = forms.ChoiceField(
        label="Тип оподаткування",
        choices=[
            ('single_tax_5', 'Платник Єдиного податку 5% 3 група\n'),
            ('vat', 'Платник ПДВ\n'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Contracts
        fields = ['start_date', 'end_date', 'tax_type']
        labels = {
            'start_date': "Час початку договору",
            'end_date': "Час закінчення договору",
        }
        widgets = {
            'start_date': forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            'end_date': forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].initial = date.today().isoformat()
        self.fields['end_date'].initial = (date.today() + timedelta(days=365)).isoformat()


class RolandForm(RoyalForm):
    doc_address = forms.ChoiceField(
        label="Адреса в документі",
        choices=[
            ('tetiiv', 'Тетіїв'),
            ('dariliv', 'Радивилів'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    full_doc_address = forms.ChoiceField(
        label="Повна адреса",
        choices=[
            ('tetiiv', '09800, Київська область, м. Тетіїв, вул. Богдана Хмельницького, 3.'),
            ('dariliv', '35500, Рівненська обл., м. Радивилів, вул. О. Невського, 71Ж.'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta(RoyalForm.Meta):
        pass


class TemplatesForm(forms.ModelForm):
    path = forms.FileField(
        label="Завантажте файл",
        widget=forms.FileInput(attrs={'type': 'file'}),
        required=True
    )

    class Meta:
        model = Templates
        fields = ['template_type', 'business_entity_type', 'name', 'path']
        labels = {
            'template_type': 'Тип шаблону',
            'business_entity_type': 'Тип СГ',
            'name': 'Назва шаблону',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


