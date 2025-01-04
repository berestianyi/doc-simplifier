from django import forms

from .models import Bank


class BankCreateForm(forms.ModelForm):
    class Meta:
        model = Bank

        fields = [
            'name',
            'mfo',
        ]
        labels = {
            'name': 'Назва банку',
            'mfo': 'МФО',
        }
        widgets = {
            'name': forms.EmailInput(attrs={
                'placeholder': 'ПуАТ «КБ «АКОРДБАНК»',
            }),
            'mfo': forms.TextInput(attrs={
                'placeholder': '380634',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class BankUpdateForm(BankCreateForm):
    class Meta(BankCreateForm.Meta):
        pass


class BankDetailForm(BankCreateForm):
    class Meta(BankCreateForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = True
