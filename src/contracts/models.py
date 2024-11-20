from django.db import models
from django.utils.translation import gettext_lazy as _


class Contracts(models.Model):
    business_entities = models.ForeignKey(
        'business_entities.BusinessEntities',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    template = models.ForeignKey(
        'contracts.Templates',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Contract {self.business_entities.name}"


class Templates(models.Model):
    class TypeEnum(models.TextChoices):
        ATP = 'ATP', _('АТП')
        OFFICE = 'OFFICE', _('Офіс')

    name = models.CharField(blank=True, null=True, max_length=100)
    type = models.CharField(
        choices=TypeEnum.choices,
        default=TypeEnum.ATP,
        blank=True,
        null=True,
        max_length=100
    )
    path = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.name
