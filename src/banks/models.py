from django.db import models
from django.utils.translation import gettext_lazy as _


class Bank(models.Model):
    name = models.CharField(_("Bank Name"), max_length=200, blank=True, default="")
    mfo = models.CharField(_("MFO"), blank=True, default="")

    def __str__(self):
        return f"Bank: {self.name}"
