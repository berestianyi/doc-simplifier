from django.db import models


class Documents(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    path = models.FileField(upload_to='uploads/', blank=True, null=True, max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    contract = models.ForeignKey(
        'contracts.Contracts',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.path
