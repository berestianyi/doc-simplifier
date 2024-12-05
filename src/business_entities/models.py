from django.db import models
from django.utils.translation import gettext_lazy as _


class Bank(models.Model):
    name = models.CharField(_("Bank Name"), max_length=200, blank=True, null=True)
    mfo = models.CharField(_("MFO"), blank=True, null=True)

    def __str__(self):
        return f"Bank: {self.name}"


class BusinessEntities(models.Model):

    class BusinessEntitiesEnum(models.TextChoices):
        TOV = "TOV", _("ТОВ")
        FOP = "FOP", _("ФОП")

    business_entity = models.CharField(
        max_length=3,
        choices=BusinessEntitiesEnum.choices,
        default=BusinessEntitiesEnum.FOP
    )
    edrpou = models.CharField(_("Code EDRPOU"), max_length=10, blank=True, unique=True, null=True)
    company_name = models.CharField(_("Company Name"), max_length=300, blank=True, null=True)
    director_name = models.CharField(_("Director Name"), max_length=300, blank=True, null=True)
    address = models.CharField(_("Address"), max_length=200, blank=True, null=True)
    email = models.EmailField(_("Email"), blank=True, null=True)
    phone = models.CharField(_("Phone"), max_length=200, blank=True, null=True)
    iban = models.CharField(_("IBAN"), max_length=200, blank=True, null=True)

    bank = models.ForeignKey('Bank', on_delete=models.CASCADE, blank=True, null=True, related_name="business_entities")

    def __str__(self):
        return f"BusinessEntity: {self.director_name}"

    def save(self, *args, **kwargs):

        if self.business_entity == BusinessEntities.BusinessEntitiesEnum.FOP:
            self.company_name = self.director_name

        super().save(*args, **kwargs)
