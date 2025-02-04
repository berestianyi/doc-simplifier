from django.db import models

from django.utils.translation import gettext_lazy as _


class Vehicles(models.Model):

    class EuroStandardEnum(models.TextChoices):
        EURO_1 = "Euro-1", _("Євро-1")
        EURO_2 = "Euro-2", _("Євро-2")
        EURO_3 = "Euro-3", _("Євро-3")
        EURO_4 = "Euro-4", _("Євро-4")
        EURO_5 = "Euro-5", _("Євро-5")
        EURO_6 = "Euro-6", _("Євро-6")
        EURO_7 = "Euro-7", _("Євро-7")

    class VehicleTypeEnum(models.TextChoices):
        PASSENGER_CAR = "Passenger Car", _("Легковий автомобіль")
        TRUCK = "Truck", _("Вантажний автомобіль")
        BUS = "Bus", _("Автобус")

    vin_code = models.CharField(max_length=100, unique=False, blank=True, null=True)
    vehicle_type = models.CharField(choices=VehicleTypeEnum.choices, blank=True, null=True)
    number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=100, blank=True, null=True)
    unladen_weight = models.CharField(max_length=100, blank=True, null=True)
    laden_weight = models.CharField(max_length=100, blank=True, null=True)
    engine_capacity = models.CharField(max_length=100, blank=True, null=True)
    number_of_seats = models.CharField(max_length=100, blank=True, null=True)
    euro = models.CharField(choices=EuroStandardEnum.choices, blank=True, null=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    def __str__(self):
        return self.vin_code


class VehicleLicences(models.Model):

    class TypeEnum(models.TextChoices):
        MAIN = "MAIN", _("Основні")
        TEMPORARY = "TEMPORARY", _("Тимчасові")

    type = models.CharField(choices=TypeEnum.choices, default=TypeEnum.MAIN)
    serial = models.CharField(max_length=50, null=True, blank=True)
    licence_number = models.CharField(max_length=50, null=True, blank=True)
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
        return f"{self.licence_number} {self.vehicle}"
