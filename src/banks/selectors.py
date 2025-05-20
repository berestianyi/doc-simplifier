from typing import List

from django.db.models import Count

from .models import Bank


class BankSelector:
    @staticmethod
    def available_banks() -> List[Bank]:
        return (
            Bank.objects
            .annotate(num_entities=Count('business_entities'))
            .order_by('-num_entities', 'name')
        )
