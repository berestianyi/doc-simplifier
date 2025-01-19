from django.db import models
from django.utils.translation import gettext_lazy as _


class BusinessEntitiesEnum(models.TextChoices):
    TOV = "TOV", _("ТОВ")
    FOP = "FOP", _("ФОП")


class BusinessEntities(models.Model):

    business_entity = models.CharField(
        max_length=3,
        choices=BusinessEntitiesEnum.choices,
        default=BusinessEntitiesEnum.FOP,

    )
    edrpou = models.CharField(_("Code EDRPOU"), max_length=10, blank=True, unique=True, null=True)
    company_name = models.CharField(_("Company Name"), max_length=300, blank=True, null=True)
    director_name = models.CharField(_("Director Name"), max_length=300, blank=True, null=True)
    address = models.CharField(_("Address"), max_length=200, blank=True, null=True)
    email = models.EmailField(_("Email"), blank=True, null=True)
    phone = models.CharField(_("Phone"), max_length=200, blank=True, null=True)
    iban = models.CharField(_("IBAN"), max_length=200, blank=True, null=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    bank = models.ForeignKey('banks.Bank', on_delete=models.SET_NULL, blank=True, null=True, related_name="business_entities")

    def __str__(self):
        return f"BusinessEntity: {self.director_name}"
