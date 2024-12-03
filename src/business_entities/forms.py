from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import BusinessEntities


def validate_edrpou(value):
    if not value.isdigit():
        raise ValidationError(_('Це поле повинно містити лише цифри.'), code='invalid')

    if BusinessEntities.objects.filter(edrpou=value).exists():
        raise ValidationError(_("Цей код ЄДРПОУ вже існує."), code='invalid')


class BusinessEntitiesForm(forms.ModelForm):
    edrpou = forms.CharField(
        required=False,
        label='ЄДРПОУ',
        max_length=10,
        min_length=8,
        validators=[validate_edrpou],
        widget=forms.TextInput(attrs={
            'placeholder': '12345678',
            'class': 'form-control',
        })
    )

    class Meta:
        model = BusinessEntities
        fields = [
            'edrpou',
            'director_name',
            'company_name',
            'address',
            'phone',
            'email',
            'iban',
        ]
        labels = {
            'director_name': 'Імʼя директора ТОВа (ПІБ)',
            'company_name': 'Назва ТОВа',
            'address': 'Адреса',
            'phone': 'Телефон',
            'email': 'Email',
            'iban': 'IBAN',
        }
        widgets = {
            'director_name': forms.TextInput(attrs={
                'placeholder': 'Іванов Іван Іванович',
                'class': 'form-control',
            }),
            'company_name': forms.TextInput(attrs={
                'placeholder': 'Google LLC',
                'class': 'form-control',
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'Україна, вул. Хрещатик, 1',
                'class': 'form-control',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+3809901234567',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@gmail.com',
                'class': 'form-control',
            }),
            'iban': forms.TextInput(attrs={
                'placeholder': 'UAXXXXXXXXXXXXXXXXXXXXXXXXXXX',
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ensure all fields have 'form-control' class for Bootstrap styling
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
