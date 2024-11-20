from django.db import models


class Documents(models.Model):
    path = models.CharField(blank=True, null=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    contract = models.ForeignKey(
        'contracts.Contracts',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.path
