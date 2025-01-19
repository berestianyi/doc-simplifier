from django import forms
from datetime import date, timedelta

from contracts.models import Contracts, Templates


class ContractTimeRangeForm(forms.Form):
    start_date = forms.DateField(
        label="Час початку договору",
        widget=forms.DateInput(attrs={"type": "date"}),
        required=True
    )
    end_date = forms.DateField(
        label="Час закінчення договору",
        widget=forms.DateInput(attrs={"type": "date"}),
        required=True
    )

    class Meta:
        model = Contracts
        fields = [
            'start_date',
            'end_date'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].initial = date.today().isoformat()
        self.fields['end_date'].initial = (date.today() + timedelta(days=365)).isoformat()

        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class TemplatesForm(forms.ModelForm):
    path = forms.FileField(
        label="Завантажте файл",
        widget=forms.FileInput(attrs={'type': 'file'}),
        required=True
    )

    class Meta:
        model = Templates
        fields = ['business_entity_type', 'name', 'path']
        labels = {
            'business_entity_type': 'Тип СГ',
            'name': 'Назва шаблону',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


