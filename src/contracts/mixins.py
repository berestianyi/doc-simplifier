from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from business_entities.models import BusinessEntitiesEnum
from .models import Templates, TemplateTypeEnum
from .services import RoyalReplacement, RolandReplacement


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

    def get_replacement_manager_class(self):
        if self.template_obj.template_type == TemplateTypeEnum.ROYAL:
            return RoyalReplacement
        return RolandReplacement
