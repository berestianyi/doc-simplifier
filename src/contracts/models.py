from django.db import models
from django.utils.translation import gettext_lazy as _


class Contracts(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    path = models.FileField(upload_to='uploads/', blank=True, null=True, max_length=256)
    business_entities = models.ForeignKey(
        'business_entities.BusinessEntities',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    template = models.ForeignKey(
        'contracts.Templates',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Contract {self.business_entities.director_name}"


class Templates(models.Model):
    class BusinessEntityTypeEnum(models.TextChoices):
        TOV = "TOV", _("ТОВ")
        FOP = "FOP", _("ФОП")

    business_entity_type = models.CharField(
        max_length=3,
        choices=BusinessEntityTypeEnum.choices,
        default=BusinessEntityTypeEnum.FOP,
        blank=True,
        null=True
    )

    name = models.CharField(blank=True, null=True, max_length=100)
    path = models.FileField(upload_to='uploads/templates/', blank=True, null=True)

    def __str__(self):
        return self.name
