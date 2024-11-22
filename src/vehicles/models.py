from django.db import models

from django.utils.translation import gettext_lazy as _


class Vehicles(models.Model):
    vin_code = models.CharField(max_length=100, unique=True, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=100, blank=True, null=True)
    unladen_weight = models.CharField(max_length=100, blank=True, null=True)
    laden_weight = models.CharField(max_length=100, blank=True, null=True)
    engine_capacity = models.CharField(max_length=100, blank=True, null=True)
    number_of_seats = models.CharField(max_length=100, blank=True, null=True)
    euro = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.vin_code


class VehicleLicences(models.Model):

    class TypeEnum(models.TextChoices):
        MAIN = "MAIN", _("Основні")
        TEMPORARY = "TEMPORARY", _("Тимчасові")

    type = models.CharField(choices=TypeEnum.choices, default=TypeEnum.MAIN)
    serial = models.CharField(max_length=50, null=True, blank=True)
    number = models.CharField(max_length=50, null=True, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    vehicle = models.ForeignKey('vehicles.Vehicles', blank=True, null=True, on_delete=models.CASCADE)
    business_entities = models.ManyToManyField(
        'business_entities.BusinessEntities',
        verbose_name=_("Vehicle Licences"),
        blank=True,
        related_name='vehicle_licences'
    )

    def __str__(self):
        return f"{self.number} {self.vehicle}"
