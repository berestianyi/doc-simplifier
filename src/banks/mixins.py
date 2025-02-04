from django.db.models import Count
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

    @staticmethod
    def available_banks():
        return (
            Bank.objects
            .annotate(num_entities=Count('business_entities'))
            .order_by('-num_entities', 'name')
        )

