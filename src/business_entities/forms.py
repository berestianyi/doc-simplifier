import re
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import BusinessEntities


def validate_edrpou(value):
    if not value.isdigit():
        raise ValidationError(_('Це поле повинно містити лише цифри.'), code='invalid')


def validate_address(value: str):
    address_components = value.replace("\n", " ").split(", ")

    patterns_to_compile = [
        r"\d{5}",
        r"[А-ЯҐЄІЇ][а-яґєіїʼ\S-]+ обл\.",
        r"м\. [А-ЯІЇЄҐІЇ][а-яіїєґʼ\S-]+(?: [А-ЯІЇЄҐ][а-яіїєґʼ\S-]+)?",
        r"кімната [А-ЯІЇЄҐІЇ][а-яіїєґʼ\S-]+(?: [А-ЯІЇЄҐ][а-яіїєґʼ\S-]+)?",
        r"[А-ЯҐЄІЇ][а-яґєіїʼ\S-]+ р-н",
        r"проспект [А-ЯІЇЄҐ][а-яіїєґ]+(?: [А-ЯІЇЄҐ][а-яіїєґ]+)?",
        r"с\. [А-ЯҐЄІЇ][а-яґєіїʼ\S\'-]+",
        r"смт\. [А-ЯҐЄІЇ][а-яґєіїʼ\S-]+",
        r"вул\. [А-ЯҐЄІЇ][а-яґєіїʼ\S-]+",
        r"буд\. \d+",
        r"кв\. \d+",
        r"офіс \d+",
        r"\d+",
    ]

    combined_pattern = re.compile(r"^(" + "|".join(patterns_to_compile) + r")$")

    for component in address_components:
        if not combined_pattern.match(component):
            raise ValidationError(
                _('Невірний формат адреси. Приклад: 01030, Київська обл., м. Київ, вул. Леонтовича, буд. 7')
            )


def validate_phone(value):
    phone_components = value.replace("\n", " ").split(", ")

    phone_patterns = [
        r"0\d{9}",
    ]

    combined_pattern = re.compile(r"^(" + "|".join(phone_patterns) + r")$")

    for phone in phone_components:
        phone = phone.strip()
        if not combined_pattern.match(phone):
            raise ValidationError(
                _('Невірний формат телефону. Приклад: 0991234567 або 0991234567,0679876543')
            )


def validate_iban(value):
    if not re.fullmatch(
            r'^UA\d{2}\d{6}\d{19}$',
            value
    ):
        raise ValidationError(
            _('Невірний формат IBAN. Приклад: UA903052992990004149123456789')
        )


class BusinessEntitiesForm(forms.ModelForm):
    address = forms.CharField(
        required=False,
        label='Адреса',
        validators=[validate_address],
        widget=forms.Textarea(attrs={
            'placeholder': '01030, м. Київ, вул. Леонтовича, офіс 7',
            'style': 'height: 40px; max-height: 120px;',
        })
    )

    phone = forms.CharField(
        required=False,
        label='Телефон',
        validators=[validate_phone],
        widget=forms.Textarea(attrs={
            'placeholder': '09901234567',
            'style': 'height: 40px; max-height: 120px;',
        })
    )

    email = forms.EmailField(
        required=False,
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@gmail.com',
        })
    )

    iban = forms.CharField(
        required=False,
        label='IBAN',
        validators=[validate_iban],
        widget=forms.TextInput(attrs={
            'placeholder': 'UAXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        })
    )

    class Meta:
        model = BusinessEntities
        fields = [
            'address',
            'phone',
            'email',
            'iban',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class FOPForm(BusinessEntitiesForm):
    edrpou = forms.CharField(
        required=False,
        label='ЄДРПОУ',
        max_length=10,
        min_length=10,
        validators=[validate_edrpou],
        widget=forms.TextInput(attrs={
            'placeholder': '1234567890',
        })
    )

    director_name = forms.CharField(
        required=False,
        label='ПІБ ФОПа',
        widget=forms.TextInput(attrs={
            'placeholder': 'Іванов Іван Іванович',
        })
    )

    class Meta(BusinessEntitiesForm.Meta):
        model = BusinessEntities
        fields = ['edrpou', 'director_name'] + BusinessEntitiesForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class FOPCreateForm(FOPForm):
    class Meta(FOPForm.Meta):
        pass


class FOPUpdateForm(FOPForm):
    class Meta(FOPForm.Meta):
        pass


class FOPDetailForm(FOPForm):
    class Meta(FOPForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = True


class TOVForm(BusinessEntitiesForm):
    edrpou = forms.CharField(
        required=False,
        label='ЄДРПОУ',
        max_length=8,
        min_length=8,
        validators=[validate_edrpou],
        widget=forms.TextInput(attrs={
            'placeholder': '12345678',
        })
    )

    director_name = forms.CharField(
        required=False,
        label='ПІБ директора',
        widget=forms.TextInput(attrs={
            'placeholder': 'Іванов Іван Іванович',
        })
    )

    company_name = forms.CharField(
        required=False,
        label='Назва ТОВа',
        widget=forms.TextInput(attrs={
            'placeholder': 'Google LLC',
        })
    )

    class Meta(BusinessEntitiesForm.Meta):
        model = BusinessEntities
        fields = ['edrpou', 'director_name', 'company_name'] + BusinessEntitiesForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class TOVCreateForm(TOVForm):
    class Meta(TOVForm.Meta):
        pass


class TOVUpdateForm(TOVForm):
    class Meta(TOVForm.Meta):
        pass


class TOVDetailForm(TOVForm):
    class Meta(TOVForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = True
