from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import User


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class ProfileForm(forms.ModelForm):
    current_password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Пароль"
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        labels = {
            'email': 'Email',
            'first_name': 'Ім`я',
            'last_name': 'Призвіще',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

    def clean_current_password(self):
        current_password = self.cleaned_data.get("current_password")
        if not self.instance.check_password(current_password):
            raise forms.ValidationError("Невірно введений пароль.")
        return current_password


class ProfileDetailForm(ProfileForm):
    class Meta(ProfileForm.Meta):

        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['disabled'] = True
