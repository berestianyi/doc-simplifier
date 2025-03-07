from django import forms


class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control forms-control-lg',
            'type': 'file'
        }),
        label='Завантажити файл з OpenDataBot'
    )

