from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_only_digits(value):

    if not value.isdigit():
        raise ValidationError(_('Це поле повинно містити лише цифри.'), code='invalid')


class BusinessEntitiesForm(forms.Form):
    edrpou = forms.CharField(
        required=False,
        label='ЄДРПОУ',
        max_length=8,
        min_length=8,
        widget=forms.TextInput(attrs={'placeholder': '12345678'}),
        validators=[validate_only_digits]
    )
    fop_name = forms.CharField(
        required=False,
        label='Імʼя ФОПа (ПІБ)',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Іванов Іван Іванович'})
    )
    director_name = forms.CharField(
        required=False,
        label='Імʼя директора ТОВа (ПІБ)',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Іванов Іван Іванович'})
    )
    company_name = forms.CharField(
        required=False,
        label='Назва ТОВа',
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Google LLC'})
    )
    address = forms.CharField(
        required=False,
        label='Адреса',
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'УкраЇна, вул. Хрещатик, 1'})
    )
    phone = forms.CharField(
        required=False,
        label='Телефон',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': '+3809901234567'})
    )
    email = forms.EmailField(
        required=False,
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'})
    )
    iban = forms.CharField(
        required=False,
        label='IBAN',
        max_length=34,
        widget=forms.TextInput(attrs={'placeholder': 'UAXXXXXXXXXXXXXXXXXXXXXXXXXXX'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
            })
