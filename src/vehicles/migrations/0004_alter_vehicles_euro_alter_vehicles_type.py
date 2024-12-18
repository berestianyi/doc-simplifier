# Generated by Django 5.1.3 on 2024-12-09 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0003_alter_vehicles_euro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicles',
            name='euro',
            field=models.CharField(blank=True, choices=[('Euro-1', 'Євро-1'), ('Euro-2', 'Євро-2'), ('Euro-3', 'Євро-3'), ('Euro-4', 'Євро-4'), ('Euro-5', 'Євро-5'), ('Euro-6', 'Євро-6'), ('Euro-7', 'Євро-7')], null=True),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='type',
            field=models.CharField(blank=True, choices=[('Passenger Car', 'Легковий автомобіль'), ('Truck', 'Вантажний автомобіль'), ('Bus', 'Автобус')], null=True),
        ),
    ]
