from django import forms


class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control form-control-lg',
            'type': 'file',
        })
    )
