from django.db import models
from django.utils.translation import gettext_lazy as _


class Bank(models.Model):
    name = models.CharField(_("Bank Name"), max_length=200, blank=True, null=True)
    mfo = models.CharField(_("MFO"), blank=True, null=True)

    def __str__(self):
        return f"Bank: {self.name}"
