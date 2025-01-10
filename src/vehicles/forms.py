import re

from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from business_entities.models import BusinessEntities
from .models import Vehicles, VehicleLicences


def validate_vin_code(value):
    if value:
        if len(value) != 17:
            raise ValidationError(_('VIN-код повинен містити рівно 17 символів.'), code='invalid')
        if not value.isalnum():
            raise ValidationError(_('VIN-код повинен бути алфавітно-цифровим.'), code='invalid')


def validate_unique_vehicle_number(value):
    if value:
        pattern = r'^[A-Za-z0-9]+$'
        if not re.match(pattern, value):
            raise ValidationError(
                _('Це поле повинно містити лише латинські літери та цифри.'),
                code='invalid'
            )


class VehiclesForm(forms.ModelForm):
    number = forms.CharField(
        required=False,
        label='Номер ТЗ',
        max_length=100,
        validators=[validate_unique_vehicle_number],
        widget=forms.TextInput(attrs={
            'placeholder': 'Введіть номер транспортного засобу',
        })
    )

    class Meta:
        model = Vehicles
        fields = [
            'number',
            'brand',
            'model',
            'year',
        ]

        labels = {
            'brand': 'Марка',
            'model': 'Модель',
            'year': 'Рік випуску',
        }

        widgets = {
            'brand': forms.TextInput(attrs={
                'placeholder': 'Введіть марку',
            }),
            'model': forms.TextInput(attrs={
                'placeholder': 'Введіть модель',
            }),
            'year': forms.TextInput(attrs={
                'placeholder': 'Введіть рік випуску',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class VehiclesCreateForm(VehiclesForm):
    vin_code = forms.CharField(
        required=False,
        label='VIN-код',
        max_length=17,
        validators=[validate_vin_code],
        widget=forms.TextInput(attrs={
            'placeholder': 'Введіть VIN-код',
        })
    )

    class Meta(VehiclesForm.Meta):
        model = Vehicles
        fields = ['vin_code', 'vehicle_type'] + VehiclesForm.Meta.fields + [
            'unladen_weight',
            'laden_weight',
            'engine_capacity',
            'number_of_seats',
            'euro',
        ]
        labels = {
            **VehiclesForm.Meta.labels,
            'vehicle_type': 'Тип транспортного засобу',
            'unladen_weight': 'Вага без навантаження',
            'laden_weight': 'Вага з навантаженням',
            'engine_capacity': 'Обʼєм двигуна',
            'number_of_seats': 'Кількість місць',
            'euro': 'Екологічний стандарт (Євро)',
        }
        widgets = {
            **VehiclesForm.Meta.widgets,
            'vehicle_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'unladen_weight': forms.TextInput(attrs={
                'placeholder': 'Введіть вагу без навантаження',
            }),
            'laden_weight': forms.TextInput(attrs={
                'placeholder': 'Введіть вагу з навантаженням',
            }),
            'engine_capacity': forms.TextInput(attrs={
                'placeholder': 'Введіть обʼєм двигуна',
            }),
            'number_of_seats': forms.TextInput(attrs={
                'placeholder': 'Введіть кількість місць',
            }),
            'euro': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class VehiclesUpdateForm(VehiclesCreateForm):
    class Meta(VehiclesCreateForm.Meta):
        pass


class VehiclesDetailForm(VehiclesCreateForm):
    class Meta(VehiclesCreateForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = True


class VehicleContractForm(VehiclesForm):
    class Meta(VehiclesForm.Meta):
        pass


class VehicleLicencesCreateForm(forms.ModelForm):
    class Meta:
        model = VehicleLicences
        fields = [
            'type',
            'serial',
            'licence_number',
            'registration_date',
            'expiration_date'
        ]
        labels = {
            'type': 'Вид технічного паспорту',
            'serial': 'Серія',
            'licence_number': 'Номер',
            'registration_date': 'Дата реєстрації',
            'expiration_date': 'Дата закінчення'
        }
        widgets = {
            'type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'serial': forms.TextInput(attrs={
                'placeholder': 'Введіть серію',
            }),
            'licence_number': forms.TextInput(attrs={
                'placeholder': 'Введіть номер ліцензії',
            }),
            'registration_date': forms.DateInput(attrs={
                'type': 'date',
            }),
            'expiration_date': forms.DateInput(attrs={
                'type': 'date',
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != 'type' and 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class VehicleLicencesUpdateForm(VehicleLicencesCreateForm):
    class Meta(VehicleLicencesCreateForm.Meta):
        pass


class VehicleLicencesDetailForm(VehicleLicencesCreateForm):
    class Meta(VehicleLicencesCreateForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = True
