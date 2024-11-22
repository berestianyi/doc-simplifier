# Generated by Django 5.1.3 on 2024-11-10 15:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('business_entities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vin_code', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
                ('number', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('brand', models.CharField(blank=True, max_length=100, null=True)),
                ('model', models.CharField(blank=True, max_length=100, null=True)),
                ('year', models.CharField(blank=True, max_length=100, null=True)),
                ('unladen_weight', models.CharField(blank=True, max_length=100, null=True)),
                ('laden_weight', models.CharField(blank=True, max_length=100, null=True)),
                ('engine_capacity', models.CharField(blank=True, max_length=100, null=True)),
                ('number_of_seats', models.CharField(blank=True, max_length=100, null=True)),
                ('euro', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleLicences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('MAIN', 'Основні'), ('TEMPORARY', 'Тимчасові')], default='MAIN')),
                ('serial', models.CharField(blank=True, max_length=50, null=True)),
                ('number', models.CharField(blank=True, max_length=50, null=True)),
                ('registration_date', models.DateField(blank=True, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('business_entities', models.ManyToManyField(blank=True, related_name='vehicle_licences', to='business_entities.businessentities', verbose_name='Vehicle Licences')),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vehicles.vehicles')),
            ],
        ),
    ]
