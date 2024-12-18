from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import BusinessEntities


def validate_edrpou(value):
    if not value.isdigit():
        raise ValidationError(_('Це поле повинно містити лише цифри.'), code='invalid')


class BusinessEntitiesCreateForm(forms.ModelForm):
    edrpou = forms.CharField(
        required=False,
        label='ЄДРПОУ',
        max_length=10,
        min_length=8,
        validators=[validate_edrpou],
        widget=forms.TextInput(attrs={
            'placeholder': '12345678',
        })
    )

    address = forms.CharField(
        label='Адреса',
        widget=forms.Textarea(attrs={
            'placeholder': 'Україна, вул. Хрещатик, 1',
            'style': 'height: 40px; max-height: 120px;',
        })
    )

    phone = forms.CharField(
        label='Телефон',
        widget=forms.Textarea(attrs={
            'placeholder': '+3809901234567',
            'style': 'height: 40px; max-height: 120px;',
        })
    )

    class Meta:
        model = BusinessEntities
        fields = [
            'business_entity',
            'edrpou',
            'director_name',
            'company_name',
            'address',
            'phone',
            'email',
            'iban',
        ]
        labels = {
            'director_name': 'ПІБ директора',
            'company_name': 'Назва ТОВа',
            'email': 'Email',
            'iban': 'IBAN',
        }
        widgets = {
            'business_entity': forms.RadioSelect(attrs={'class': 'btn-check'}),
            'director_name': forms.TextInput(attrs={
                'placeholder': 'Іванов Іван Іванович',
            }),
            'company_name': forms.TextInput(attrs={
                'placeholder': 'Google LLC',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@gmail.com',
            }),
            'iban': forms.TextInput(attrs={
                'placeholder': 'UAXXXXXXXXXXXXXXXXXXXXXXXXXXX',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class BusinessEntitiesUpdateForm(BusinessEntitiesCreateForm):
    class Meta(BusinessEntitiesCreateForm.Meta):
        pass
