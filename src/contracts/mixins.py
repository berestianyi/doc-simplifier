from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from src.business_entities.models import BusinessEntitiesEnum
from .models import Templates


class TemplateMixin:
    @cached_property
    def template_obj(self) -> Templates | None:
        template_id = self.kwargs.get("template_id")
        if template_id is None:
            return None
        return get_object_or_404(Templates, pk=template_id)

    @staticmethod
    def filter_by_business_entity(business_entity, queryset):
        if business_entity.business_entity == BusinessEntitiesEnum.FOP:
            queryset = queryset.filter(
                business_entity_type=BusinessEntitiesEnum.FOP
            )
        elif business_entity.business_entity == BusinessEntitiesEnum.TOV:
            queryset = queryset.filter(
                business_entity_type=BusinessEntitiesEnum.TOV
            )
        return queryset
