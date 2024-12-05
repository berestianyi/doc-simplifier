from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Vehicles, VehicleLicences


def validate_vin_code(value):
    if value:
        if len(value) != 17:
            raise ValidationError(_('VIN-код повинен містити рівно 17 символів.'), code='invalid')
        if not value.isalnum():
            raise ValidationError(_('VIN-код повинен бути алфавітно-цифровим.'), code='invalid')
        if Vehicles.objects.filter(vin_code=value).exists():
            raise ValidationError(_("Цей VIN-код вже існує."), code='invalid')


def validate_unique_vehicle_number(value):
    if value and Vehicles.objects.filter(number=value).exists():
        raise ValidationError(_("Цей номер транспортного засобу вже існує."), code='invalid')


class VehiclesCreateForm(forms.ModelForm):
    vin_code = forms.CharField(
        required=False,
        label='VIN-код',
        max_length=17,
        validators=[validate_vin_code],
        widget=forms.TextInput(attrs={
            'placeholder': 'Введіть VIN-код',
            'class': 'form-control',
        })
    )
    number = forms.CharField(
        required=False,
        label='Номер',
        max_length=100,
        validators=[validate_unique_vehicle_number],
        widget=forms.TextInput(attrs={
            'placeholder': 'Введіть номер транспортного засобу',
            'class': 'form-control',
        })
    )

    class Meta:
        model = Vehicles
        fields = [
            'vin_code',
            'type',
            'number',
            'brand',
            'model',
            'year',
            'unladen_weight',
            'laden_weight',
            'engine_capacity',
            'number_of_seats',
            'euro',
        ]
        labels = {
            'type': 'Тип транспортного засобу',
            'brand': 'Марка',
            'model': 'Модель',
            'year': 'Рік випуску',
            'unladen_weight': 'Вага без навантаження',
            'laden_weight': 'Вага з навантаженням',
            'engine_capacity': 'Обʼєм двигуна',
            'number_of_seats': 'Кількість місць',
            'euro': 'Екологічний стандарт (Євро)',
        }
        widgets = {
            'type': forms.TextInput(attrs={
                'placeholder': 'Введіть тип транспортного засобу',
            }),
            'brand': forms.TextInput(attrs={
                'placeholder': 'Введіть марку',
            }),
            'model': forms.TextInput(attrs={
                'placeholder': 'Введіть модель',
            }),
            'year': forms.TextInput(attrs={
                'placeholder': 'Введіть рік випуску',
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
            'euro': forms.TextInput(attrs={
                'placeholder': 'Введіть екологічний стандарт (Євро)',
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


class VehicleLicencesCreateForm(forms.ModelForm):
    class Meta:
        model = VehicleLicences
        fields = [
            'type',
            'serial',
            'number',
            'registration_date',
            'expiration_date',
            'vehicle',
            'business_entities',
        ]
        labels = {
            'type': 'Тип ліцензії',
            'serial': 'Серія',
            'number': 'Номер',
            'registration_date': 'Дата реєстрації',
            'expiration_date': 'Дата закінчення',
            'vehicle': 'Транспортний засіб',
            'business_entities': 'Юридичні особи',
        }
        widgets = {
            'type': forms.RadioSelect(attrs={'class': 'btn-check'}),
            'serial': forms.TextInput(attrs={
                'placeholder': 'Введіть серію',
            }),
            'number': forms.TextInput(attrs={
                'placeholder': 'Введіть номер ліцензії',
            }),
            'registration_date': forms.DateInput(attrs={
                'type': 'date',
            }),
            'expiration_date': forms.DateInput(attrs={
                'type': 'date',
            }),
            'vehicle': forms.Select(attrs={
                'class': 'form-control',
            }),
            'business_entities': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != 'type' and 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class VehicleLicencesUpdateForm(VehicleLicencesCreateForm):
    class Meta(VehicleLicencesCreateForm.Meta):
        pass
