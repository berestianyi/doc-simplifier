from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from business_entities.models import BusinessEntities
from .models import Vehicles, VehicleLicences


class VehicleMixin:

    @cached_property
    def vehicle(self):
        vehicle_id = self.kwargs.get("vehicle_id")
        if vehicle_id is None:
            return None
        return get_object_or_404(Vehicles, pk=vehicle_id)

    @cached_property
    def vehicle_licence(self):
        vehicle_id = self.kwargs.get("vehicle_id")
        if vehicle_id is None:
            return None
        vehicle = get_object_or_404(Vehicles, id=vehicle_id)
        licence = get_object_or_404(VehicleLicences, vehicle=vehicle)
        if licence is None:
            return None
        return licence

    @staticmethod
    def vehicles_without_business_entities(business_entity):
        owned_vehicle_ids = VehicleLicences.objects.filter(
            business_entities=business_entity
        ).values_list('vehicle_id', flat=True)
        unowned_vehicles = Vehicles.objects.exclude(id__in=owned_vehicle_ids)

        return unowned_vehicles

    @staticmethod
    def vehicles_with_business_entity(business_entity: BusinessEntities):
        return Vehicles.objects.filter(vehiclelicences__business_entities=business_entity).distinct()
