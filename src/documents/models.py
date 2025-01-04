from django.db import models


class Documents(models.Model):
    path = models.FileField(upload_to='uploads/', blank=True, null=True, max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    contract = models.ForeignKey(
        'contracts.Contracts',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.path
