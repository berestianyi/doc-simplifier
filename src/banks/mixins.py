from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from .models import Bank


class BankMixin:
    @cached_property
    def bank(self):
        bank_id = self.kwargs.get("bank_id")
        if bank_id is None:
            return None
        return get_object_or_404(Bank, pk=bank_id)

