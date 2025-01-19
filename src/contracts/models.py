from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _

from business_entities.models import BusinessEntitiesEnum


class Contracts(models.Model):
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
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)

    def __str__(self):
        return f"Contract {self.business_entities.director_name}"


class Templates(models.Model):

    business_entity_type = models.CharField(
        max_length=3,
        choices=BusinessEntitiesEnum.choices,
        default=BusinessEntitiesEnum.FOP,
        blank=True,
        null=True
    )
    name = models.CharField(blank=True, null=True, max_length=100)
    path = models.FileField(upload_to='uploads/templates/', blank=True, null=True)

    def __str__(self):
        return self.name
