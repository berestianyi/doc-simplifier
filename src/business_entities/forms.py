from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import BusinessEntities


def validate_edrpou(value):
    if not value.isdigit():
        raise ValidationError(_('Це поле повинно містити лише цифри.'), code='invalid')


class BusinessEntitiesCreateForm(forms.ModelForm):

    address = forms.CharField(
        required=False,
        label='Адреса',
        widget=forms.Textarea(attrs={
            'placeholder': 'Україна, вул. Хрещатик, 1',
            'style': 'height: 40px; max-height: 120px;',
        })
    )

    phone = forms.CharField(
        required=False,
        label='Телефон',
        widget=forms.Textarea(attrs={
            'placeholder': '+3809901234567',
            'style': 'height: 40px; max-height: 120px;',
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
        labels = {
            'email': 'Email',
            'iban': 'IBAN',
        }
        widgets = {
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


class FOPCreateForm(BusinessEntitiesCreateForm):
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

    class Meta(BusinessEntitiesCreateForm.Meta):
        model = BusinessEntities
        fields = ['edrpou', 'director_name'] + BusinessEntitiesCreateForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class FOPUpdateForm(FOPCreateForm):
    class Meta(FOPCreateForm.Meta):
        pass


class FOPDetailForm(FOPCreateForm):
    class Meta(FOPCreateForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = True


class TOVCreateForm(BusinessEntitiesCreateForm):

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

    class Meta(BusinessEntitiesCreateForm.Meta):
        model = BusinessEntities
        fields = ['edrpou', 'director_name', 'company_name'] + BusinessEntitiesCreateForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class TOVUpdateForm(TOVCreateForm):
    class Meta(TOVCreateForm.Meta):
        pass


class TOVDetailForm(TOVCreateForm):
    class Meta(TOVCreateForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = True
